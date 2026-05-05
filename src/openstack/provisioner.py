from warnings import warn

from rich.console import Console
from rich.progress import track

from src.openstack.nova_api import NovaApi
from src.openstack.repo import VirtualMachinesRepo


class NovaProvisioner:
    def __init__(self, conf_file: str):
        self._nova_api = NovaApi(conf_file=conf_file)

    def provision(
        self,
        repo: VirtualMachinesRepo,
        raise_error: bool = True,
        wait_active: bool = True,
        wait_sec: int = 120,
    ):
        for vm in track(repo._list, description="VM creating"):
            try:
                vm = self._nova_api.create_virtual_machine(vm)
            except Exception as error:
                message = f"{vm.name} : {error}"
                if raise_error:
                    raise Exception(message)
                warn(message)

        if wait_active is False:
            return

        console = Console()
        with console.status("Waiting VM become active"):
            return self._nova_api.wait_virtual_machine_status(
                repo._list,
                wait_sec=wait_sec,
            )

    def find(self, repo: VirtualMachinesRepo):
        for vm in repo._list:
            vm.id = self._nova_api.virtual_machine_name_to_id(vm.name)

    def erase(self, repo: VirtualMachinesRepo, raise_error: bool = True):
        self.find(repo=repo)
        for vm in track(repo._list, description="VM deleting"):
            try:
                self._nova_api.delete_virtual_machine(vm)
            except Exception as error:
                message = f"{vm.name} : {error}"
                if raise_error:
                    raise Exception(message)
                warn(message)
