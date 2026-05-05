from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class VirtualMachine:
    name: str
    image: str
    flavor: str
    network_vmi_tuples: list[tuple[Any, Any]] | None = None
    id: str | None = None
    created: str | None = None  # TODO: parse to datetime
    updated: str | None = None  # TODO: parse to datetime
    availability_zone: int | None = None
    status: str | None = None
    metadata: dict | None = None
    disk_config: str = "AUTO"
    vm_state: str | None = None
    power_state: int | None = None
    user_data: str | None = None
