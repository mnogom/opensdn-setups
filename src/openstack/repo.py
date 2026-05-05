from rich.console import Console
from rich.table import Table

from src.openstack.dto import VirtualMachine


class VirtualMachinesRepo:
    def __init__(self):
        self._list: list[VirtualMachine] = []

    def create_virtual_machine(
        self,
        *,
        name: str,
        flavor_name: str,
        image_name: str,
        network_vmi_tuples: list[tuple[str, str]],
        user_data: str | None = None,
        availability_zone_id: int | None = None,
    ) -> VirtualMachine:
        virtual_machine = VirtualMachine(
            name=name,
            image=image_name,
            flavor=flavor_name,
            user_data=user_data,
            availability_zone=availability_zone_id,
            network_vmi_tuples=network_vmi_tuples,
        )
        self._list.append(virtual_machine)
        return virtual_machine

    def show_list(self):
        table = Table(title="[bold underline green]Virtual Machines")

        table.add_column("uuid", no_wrap=True, style="magenta")
        table.add_column("name", no_wrap=True)
        table.add_column("availability zone", no_wrap=True)

        for vm in self._list:
            table.add_row(vm.id, vm.name, f"{vm.availability_zone}")

        console = Console()
        console.print(table)
