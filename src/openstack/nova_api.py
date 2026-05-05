import base64
import configparser
import time
from typing import Any
from warnings import warn

import requests

from src.openstack.dto import VirtualMachine


class NovaApi:
    def __init__(self, conf_file: str):
        cfg_parser = configparser.ConfigParser(strict=False)
        cfg_parser.read(conf_file)
        self._domain = cfg_parser.get("os-global", "DOMAIN")
        self._tenant = cfg_parser.get("os-global", "TENANT")
        self._nova_server = cfg_parser.get("nova", "NOVA_SERVER")
        self._nova_proto = cfg_parser.get("nova", "NOVA_PROTOCOL")
        self._nova_port = cfg_parser.get("nova", "NOVA_PORT")
        self._nova_url = cfg_parser.get("nova", "NOVA_URL")
        self._keystone_proto = cfg_parser.get("auth", "AUTHN_PROTOCOL")
        self._keystone_server = cfg_parser.get("auth", "AUTHN_SERVER")
        self._keystone_port = cfg_parser.get("auth", "AUTHN_PORT")
        self._keystone_url = cfg_parser.get("auth", "AUTHN_URL")
        self._user = cfg_parser.get("auth", "AUTHN_USER")
        self._password = cfg_parser.get("auth", "AUTHN_PASSWORD")
        self._images = dict(cfg_parser.items("nova.images"))
        self._flavors = dict(cfg_parser.items("nova.flavors"))
        self._availability_zones = cfg_parser.get(
            "nova.availability-zones", "ZONES"
        ).split(",")
        self._compute_nodes = cfg_parser.get("nova.compute-nodes", "NODES").split(",")

        self._auth_token = None

    def get_image_id(self, name: str) -> str:
        image_id = self._images.get(name)
        if image_id is None:
            raise Exception(
                (
                    f"Can't find image with name '{name}'. "
                    "Make sure that in config-file there is "
                    "section '[images]' with row "
                    f"'{name.upper()} = <some-id>'"
                )
            )
        return image_id

    def get_image_name(self, id_: str) -> str:
        for image_name, image_id in self._images.items():
            if image_id == id_:
                return image_name
        return f"Unknown[{id_}]"

    def get_flavor_id(self, name: str) -> str:
        flavor_id = self._flavors.get(name)
        if flavor_id is None:
            raise Exception(
                (
                    f"Can't find flavor with name '{name}'. "
                    "Make sure that in config-file there is "
                    "section '[flavors]' with row "
                    f"'{name.upper()} = <some-id>'"
                )
            )
        return flavor_id

    def get_flavor_name(self, id_: str) -> str:
        for flavor_name, flavor_id in self._flavors.items():
            if flavor_id == id_:
                return flavor_name
        return f"Unknown[{id_}]"

    def get_availability_zone_name(self, id_: int) -> str:
        if id_ > len(self._availability_zones) - 1:
            raise Exception(
                (
                    f"Can't find availability zone with index '{id_}'. "
                    "Make sure that in config-file there is "
                    "section '[nova.availability-zones]' with row "
                    f"'ZONES = zone1,zone2,zone3'"
                )
            )

        az_name = self._availability_zones[id_]
        return az_name

    def get_compute_node_address(self, id_: int) -> str:
        if id_ > len(self._compute_nodes) - 1:
            raise Exception(
                (
                    f"Can't find compute node with index '{id_}'. "
                    "Make sure that in config-file there is "
                    "section '[nova.compute-nodes]' with row "
                    f"'NODES = ip1,ip2,ip3'"
                )
            )

        compute_node_ip = self._compute_nodes[id_]
        return compute_node_ip

    def _get_auth_body(self) -> dict[str, Any]:
        return {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": self._user,
                            "domain": {
                                "name": self._domain,
                            },
                            "password": self._password,
                        }
                    },
                },
                "scope": {
                    "project": {
                        "domain": {
                            "name": self._domain,
                        },
                        "name": self._tenant,
                    }
                },
            }
        }

    @staticmethod
    def _get_headers(extra_headers: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "VncApi",
            "Accept": "*/*",
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _is_valid_token(self) -> bool:
        if self._auth_token is None:
            return False
        url = f"{self._keystone_proto}://{self._keystone_server}:{self._keystone_port}{self._keystone_url}"
        headers = self._get_headers(
            extra_headers={
                "X-Auth-Token": self._auth_token,
                "X-Subject-Token": self._auth_token,
            }
        )
        response = requests.head(url, headers=headers)
        if 200 <= response.status_code < 300:
            return True
        return False

    def _update_token(self) -> None:
        url = f"{self._keystone_proto}://{self._keystone_server}:{self._keystone_port}{self._keystone_url}"
        response = requests.post(
            url, headers=self._get_headers(), json=self._get_auth_body()
        )
        assert 200 <= response.status_code < 300
        self._auth_token = response.headers["X-Subject-Token"]

    def _revoke_token(self) -> None:
        url = f"{self._keystone_proto}://{self._keystone_server}:{self._keystone_port}{self._keystone_url}"
        if self._is_valid_token() is False:
            return
        headers = self._get_headers(
            extra_headers={
                "X-Auth-Token": self._auth_token,
                "X-Subject-Token": self._auth_token,
            }
        )
        response = requests.delete(url, headers=headers)
        if response.status_code >= 300:
            warn("Can't revoke token. Idk why")

    @property
    def token(self):
        if self._is_valid_token() is False:
            self._update_token()
        return self._auth_token

    def _request_nova_api(
        self,
        url: str,
        method: str = "get",
        json: dict | None = None,
        extra_headers: dict | None = None,
    ) -> dict | None:
        if extra_headers is not None:
            extra_headers = extra_headers.copy()
        else:
            extra_headers = {}
        extra_headers["X-Auth-Token"] = self.token
        response = requests.request(
            method=method, url=url, json=json, headers=self._get_headers(extra_headers)
        )
        if response.status_code >= 400:
            raise Exception(
                f"Got '{response.status_code}' from '{url}': {response.text}"
            )
        if response.status_code == 204:
            return
        return response.json()

    def list_virtual_machine(self, name: str | None = None) -> list[VirtualMachine]:
        query = "" if name is None else f"name={name}"
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers/detail?{query}"
        data = self._request_nova_api(url=url)
        virtual_machines = []

        for server in data["servers"]:
            if name is None or server["name"].startswith(name):
                flavor = self.get_flavor_name(server["flavor"]["id"])
                image = self.get_image_name(server["image"]["id"])
                virtual_machines.append(
                    VirtualMachine(
                        id=server["id"],
                        name=server["name"],
                        image=image,
                        flavor=flavor,
                        created=server["created"],
                        updated=server["updated"],
                        availability_zone=server[
                            "OS-EXT-AZ:availability_zone"
                        ],  # TODO: make unify AZ in VM (sometimes it is str, sometimes - int)
                        status=server["status"],
                        metadata=server["metadata"],
                        disk_config=server["OS-DCF:diskConfig"],
                        vm_state=server["OS-EXT-STS:vm_state"],
                        power_state=server["OS-EXT-STS:power_state"],
                    )
                )
        return virtual_machines

    def virtual_machine_name_to_id(self, name: str):
        vm_list = self.list_virtual_machine(name)
        if len(vm_list) == 1:
            return vm_list[0].id
        else:
            # query by name is just match-filter. Be sure to get exactly vm by name
            # If name is not unique - sorry. We will pick the first one...
            for filtered_virtual_machine in vm_list:
                if filtered_virtual_machine.name == name:
                    return filtered_virtual_machine.id

    def get_virtual_machine(self, id) -> VirtualMachine:
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers/{id}"
        data = self._request_nova_api(url)
        server = data["server"]
        flavor = self.get_flavor_name(server["flavor"]["id"])
        image = self.get_image_name(server["image"]["id"])
        return VirtualMachine(
            id=server["id"],
            name=server["name"],
            image=image,
            flavor=flavor,
            created=server["created"],
            updated=server["updated"],
            availability_zone=server[
                "OS-EXT-AZ:availability_zone"
            ],  # TODO: make unify AZ in VM (sometimes it is str, sometimes - int)
            status=server["status"],
            metadata=server["metadata"],
            disk_config=server["OS-DCF:diskConfig"],
            vm_state=server["OS-EXT-STS:vm_state"],
            power_state=server["OS-EXT-STS:power_state"],
        )

    def create_virtual_machine(
        self,
        virtual_machine: VirtualMachine,
    ) -> VirtualMachine:
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers"
        networks = [{"uuid": "", "port": ""}]

        networks = []
        for network, port in virtual_machine.network_vmi_tuples:
            # NOTE: make uuid as lazy without vnc_api class dependencies
            networks.append({"uuid": network.uuid, "port": port.uuid})

        server = {
            "name": virtual_machine.name,
            "imageRef": self.get_image_id(virtual_machine.image),
            "flavorRef": self.get_flavor_id(virtual_machine.flavor),
            "networks": networks,
            "OS-DCF:diskConfig": virtual_machine.disk_config,
            "security_groups": [],
        }
        if virtual_machine.user_data is not None:
            server["user_data"] = base64.b64encode(
                virtual_machine.user_data.encode("utf-8")
            ).decode("utf-8")
        if virtual_machine.availability_zone is not None:
            server["availability_zone"] = self.get_availability_zone_name(
                virtual_machine.availability_zone
            )

        data = {"server": server}
        data_updated = self._request_nova_api(url, method="post", json=data)
        id_ = data_updated["server"]["id"]
        virtual_machine.id = id_
        return virtual_machine

    def wait_virtual_machine_status(
        self,
        virtual_machines_list: list[VirtualMachine],
        status: str = "ACTIVE",
        wait_sec: int = 120,
    ) -> list[VirtualMachine]:
        if len(virtual_machines_list) == 0:
            return []
        start = time.monotonic()
        count = 0
        total = len(virtual_machines_list)
        while True:
            time.sleep(1)
            for virtual_machine in virtual_machines_list:
                virtual_machine = self.get_virtual_machine(virtual_machine.id)
                if virtual_machine.status == status:
                    count += 1
                if count == total:
                    return virtual_machines_list
                if time.monotonic() - start > wait_sec:
                    raise TimeoutError(
                        f"Virtual machine '{virtual_machine.id}' can't become ACTIVE for in"
                        f"{wait_sec} secs. Now in status: {virtual_machine.status}"
                    )

    def delete_virtual_machine(self, virtual_machine: VirtualMachine) -> None:
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers/{virtual_machine.id}"
        self._request_nova_api(url, method="delete")

    def get_serial_console(self, virtual_machine: VirtualMachine) -> str:
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers/{virtual_machine.id}/remote-consoles"
        data = {"remote_console": {"type": "serial", "protocol": "serial"}}
        headers = self._get_headers({"OpenStack-API-Version": "compute 2.8"})
        data = self._request_nova_api(
            url, method="post", json=data, extra_headers=headers
        )
        return data["remote_console"]["url"]

    def get_vnc_console(self, virtual_machine: VirtualMachine) -> str:
        url = f"{self._nova_proto}://{self._nova_server}:{self._nova_port}{self._nova_url}/servers/{virtual_machine.id}/remote-consoles"
        data = {"remote_console": {"type": "novnc", "protocol": "vnc"}}
        headers = self._get_headers({"OpenStack-API-Version": "compute 2.8"})
        data = self._request_nova_api(
            url, method="post", json=data, extra_headers=headers
        )
        url = data["remote_console"]["url"]
        url = f"{url}&scale=true"
        return url
