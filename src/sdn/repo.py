from rich.console import Console
from rich.table import Table
from vnc_api import vnc_api

from src.sdn.constants import (
    VMI_NETWORK_ROUTER_INTERFACE,
    AllowAddressPairMode,
    IPAMDNSMethod,
    IPAMSubnetMethod,
    LogicalRouterType,
    NetworkAddressAllocationMode,
    NextHopType,
    PolicyRuleDirection,
    PolicyRuleEtherType,
    PolicyRuleProtocols,
)
from src.sdn.resources import LazyLogicalRouter


class SdnReourcesRepo:
    def __init__(self):
        self._list = []

    def create_ipam(
        self,
        *,
        fq_name: str,
        ipam_subnet_method: IPAMSubnetMethod = IPAMSubnetMethod.USER_DEFINED_SUBNET,
        ipam_dns_method: IPAMDNSMethod = IPAMDNSMethod.DEFAULT_DNS_SERVER,
        dhcp_code_value_tuples: list[tuple[str, str]] | None = None,
    ) -> vnc_api.NetworkIpam:

        dhcp_option_list = None
        if dhcp_code_value_tuples is not None:
            dhcp_option_list = vnc_api.DhcpOptionsListType()
            for code, value in dhcp_code_value_tuples:
                dhcp_option_list.add_dhcp_option(
                    vnc_api.DhcpOptionType(
                        dhcp_option_name=code,
                        dhcp_option_value=value,
                    )
                )

        ipam_type = vnc_api.IpamType(
            ipam_dns_method=ipam_dns_method,
            dhcp_option_list=dhcp_option_list,
        )
        ipam = vnc_api.NetworkIpam(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            ipam_subnet_method=ipam_subnet_method,
            network_ipam_mgmt=ipam_type,
        )
        self._list.append(ipam)
        return ipam

    def create_route_table(
        self, *, fq_name: str, prefix_nh_tuples: list[tuple[str, str]]
    ):
        routes = vnc_api.RouteTableType()
        for prefix, nh in prefix_nh_tuples:
            routes.add_route(
                vnc_api.RouteType(
                    prefix=prefix,
                    next_hop=nh,
                    next_hop_type=NextHopType.IP_ADDRESS,
                )
            )
        route_table = vnc_api.RouteTable(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
        )
        route_table.set_routes(routes)
        route_table
        self._list.append(route_table)
        return route_table

    def create_virtual_network(
        self,
        *,
        fq_name: str,
        cidr_list: list[str],
        ipam: vnc_api.NetworkIpam,
        address_allocation_mode: NetworkAddressAllocationMode = NetworkAddressAllocationMode.USER_DEFINED_SUBNET_ONLY,
        addr_from_start: bool = True,
        fabric_snat: bool = False,
        route_table: vnc_api.RouteTable | None = None,  # TODO: make list
        dhcp_code_value_tuples: list[tuple[str, str]] | None = None,
    ) -> vnc_api.VirtualNetwork:
        dhcp_option_list = None
        if dhcp_code_value_tuples is not None:
            dhcp_option_list = vnc_api.DhcpOptionsListType()
            for code, value in dhcp_code_value_tuples:
                dhcp_option_list.add_dhcp_option(
                    vnc_api.DhcpOptionType(
                        dhcp_option_name=code,
                        dhcp_option_value=value,
                    )
                )

        ipam_subnets = []
        for cidr in cidr_list:
            ip_prefix, ip_prefix_len = cidr.split("/")
            # TODO: use 'self._create_address_type' instead
            subnet = vnc_api.SubnetType(
                ip_prefix=ip_prefix, ip_prefix_len=ip_prefix_len
            )
            ipam_subnets.append(
                vnc_api.IpamSubnetType(
                    subnet=subnet,
                    addr_from_start=addr_from_start,
                    dhcp_option_list=dhcp_option_list,
                )
            )

        virtual_network_subnet = vnc_api.VnSubnetsType(ipam_subnets=ipam_subnets)

        virtual_network = vnc_api.VirtualNetwork(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            address_allocation_mode=address_allocation_mode,
            fabric_snat=fabric_snat,
        )

        virtual_network.add_network_ipam(
            ipam,
            virtual_network_subnet,
        )

        if route_table is not None:
            virtual_network.add_route_table(route_table)

        self._list.append(virtual_network)
        return virtual_network

    def _create_address_type(self, cidr: str | None) -> vnc_api.AddressType:
        if cidr is None:
            address_type = vnc_api.AddressType(
                security_group="local",
            )
        else:
            ip_prefix, ip_prefix_len = cidr.split("/")
            ip_prefix_len = int(ip_prefix_len)
            address_type = vnc_api.AddressType(
                subnet=vnc_api.SubnetType(
                    ip_prefix=ip_prefix,
                    ip_prefix_len=ip_prefix_len,
                )
            )
        return address_type

    def create_policy_rule(
        self,
        *,
        direction: PolicyRuleDirection,
        protocol: PolicyRuleProtocols,
        ethertype: PolicyRuleEtherType,
        src_cidr: str | None = None,
        src_ports: list[int, int],
        dst_ports: list[int, int],
        dst_cidr: str | None = None,
    ) -> vnc_api.PolicyRuleType:
        src_address_type = self._create_address_type(src_cidr)
        dst_address_type = self._create_address_type(dst_cidr)

        return vnc_api.PolicyRuleType(
            direction=direction,
            protocol=protocol,
            ethertype=ethertype,
            src_addresses=[src_address_type],
            src_ports=[
                vnc_api.PortType(
                    start_port=src_ports[0],
                    end_port=src_ports[1],
                ),
            ],
            dst_addresses=[dst_address_type],
            dst_ports=[
                vnc_api.PortType(
                    start_port=dst_ports[0],
                    end_port=dst_ports[1],
                ),
            ],
        )

    def create_security_group(
        self,
        *,
        fq_name: str,
        policy_rule: list[vnc_api.PolicyRuleType],
    ) -> vnc_api.SecurityGroup:
        security_group = vnc_api.SecurityGroup(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            security_group_entries=vnc_api.PolicyEntriesType(
                policy_rule=policy_rule,
            ),
        )
        self._list.append(security_group)
        return security_group

    def create_interface_route_table(
        self,
        *,
        fq_name: str,
        prefix_list: list[str],
    ) -> vnc_api.InterfaceRouteTable:
        route_table_type = vnc_api.RouteTableType()
        for prefix in prefix_list:
            route_table_type.add_route(vnc_api.RouteType(prefix=prefix))
        interface_route_table = vnc_api.InterfaceRouteTable(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            interface_route_table_routes=route_table_type,
        )
        self._list.append(interface_route_table)
        return interface_route_table

    def create_virtual_machine_interface(
        self,
        *,
        fq_name: str,
        virtual_network: vnc_api.VirtualNetwork,
        port_security_enabled: bool = False,
        security_groups: list[vnc_api.SecurityGroup] | None = None,
        virtual_machine_interface_device_owner: str = "",
        interface_route_table: vnc_api.InterfaceRouteTable | None = None,  # TODO: make list
        dhcp_code_value_tuples: list[tuple[str, str]] | None = None,
        address_pairs: list[tuple[str, str, AllowAddressPairMode]] | None = None,
    ) -> vnc_api.VirtualMachineInterface:
        """
        address_pairs: [(ip/mask, mac, mode)]. mode - Active-Active / Active-Standby
        """

        dhcp_option_list = None
        if dhcp_code_value_tuples is not None:
            dhcp_option_list = vnc_api.DhcpOptionsListType()
            for code, value in dhcp_code_value_tuples:
                dhcp_option_list.add_dhcp_option(
                    vnc_api.DhcpOptionType(
                        dhcp_option_name=code,
                        dhcp_option_value=value,
                    )
                )
        address_pair_list = None
        if address_pairs is not None:
            address_pair_list = vnc_api.AllowedAddressPairs()
            for cidr, mac, mode in address_pairs:
                ip_prefix, ip_prefix_len = cidr.split("/")
                ip_address = vnc_api.SubnetType(
                    ip_prefix=ip_prefix, ip_prefix_len=ip_prefix_len
                )
                address_pair_list.add_allowed_address_pair(
                    vnc_api.AllowedAddressPair(
                        ip=ip_address,
                        mac=mac,
                        mode=mode,
                    )
                )

        virtual_machine_inetrface = vnc_api.VirtualMachineInterface(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            virtual_machine_interface_device_owner=VMI_NETWORK_ROUTER_INTERFACE,
            port_security_enabled=port_security_enabled,
            virtual_machine_interface_dhcp_option_list=dhcp_option_list,
            virtual_machine_interface_allowed_address_pairs=address_pair_list,
        )
        virtual_machine_inetrface.add_virtual_network(virtual_network)

        if virtual_machine_interface_device_owner is not None:
            virtual_machine_inetrface.set_virtual_machine_interface_device_owner(
                virtual_machine_interface_device_owner
            )

        if port_security_enabled:
            security_groups = security_groups or []
            for sg in security_groups:
                virtual_machine_inetrface.add_security_group(sg)
        self._list.append(virtual_machine_inetrface)

        if interface_route_table is not None:
            virtual_machine_inetrface.add_interface_route_table(interface_route_table)

        return virtual_machine_inetrface

    def create_instance_ip(
        self,
        *,
        name: str,
        instance_ip_address: str,
        virtual_network: vnc_api.VirtualNetwork,
        virtual_machine_interface: vnc_api.VirtualMachineInterface,
    ) -> vnc_api.InstanceIp:
        instance_ip = vnc_api.InstanceIp(
            name=name,
            instance_ip_address=instance_ip_address,
        )
        instance_ip.add_virtual_network(virtual_network)
        instance_ip.add_virtual_machine_interface(virtual_machine_interface)
        self._list.append(instance_ip)
        return instance_ip

    def create_logical_router(
        self,
        *,
        fq_name: str,
        virtual_machine_interfaces: list[vnc_api.VirtualMachineInterface],
        logical_router_type: LogicalRouterType,
        route_targets: list[str] | None = None,
        vxlan_network_identifier: str | None = None,
    ) -> LazyLogicalRouter:
        route_targets = route_targets or []
        configured_route_target_list = vnc_api.RouteTargetList()
        for rt in route_targets:
            configured_route_target_list.add_route_target(f"target:{rt}")

        logical_router = LazyLogicalRouter(
            fq_name=fq_name.split(":", 2),
            parent_type="project",
            configured_route_target_list=configured_route_target_list,
            vxlan_network_identifier=vxlan_network_identifier,
            logical_router_type=logical_router_type,
            id_perms=vnc_api.IdPermsType(enable=True, user_visible=True),
        )
        for vmi in virtual_machine_interfaces:
            logical_router.lazy_add_virtual_machine_interface(vmi)

        self._list.append(logical_router)
        return logical_router

    def show_list(self):
        table = Table(title="[bold underline green]SDN Reources")

        table.add_column("uuid", no_wrap=True, style="magenta")
        table.add_column("type", no_wrap=True)
        table.add_column("fq_name", no_wrap=True)

        for res in self._list:
            table.add_row(res.uuid, res._type, res.get_fq_name_str())

        console = Console()
        console.print(table)
