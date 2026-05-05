from vnc_api import vnc_api


class LazyLogicalRouter(vnc_api.LogicalRouter):
    _lazy_vmi_list = None

    def lazy_add_virtual_machine_interface(
        self,
        vmi: vnc_api.VirtualMachineInterface,
    ):
        if self._lazy_vmi_list is None:
            self._lazy_vmi_list = [vmi]
        else:
            self._lazy_vmi_list.append(vmi)

    def serialize_to_json(self, field_names: set | None = None):
        if isinstance(field_names, set):
            if getattr(self, "_lazy_vmi_list") is not None:
                for vmi in self._lazy_vmi_list:
                    self.add_virtual_machine_interface(vmi)
                    field_names.add("virtual_machine_interface_refs")
        serialized = super().serialize_to_json(field_names)
        return serialized
