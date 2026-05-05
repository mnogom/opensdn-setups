from dataclasses import dataclass

from vnc_api import vnc_api

from src.sdn.vnc_api_gen import WrappedVncApi


@dataclass(slots=True, frozen=True)
class RoutingInstanceDTO:
    fq_name: str
    parent_lr: list[str]


def get_routing_instances(vnc: WrappedVncApi, prefix: str) -> list[RoutingInstanceDTO]:
    fitlered_lr = filter(
        lambda lr: lr.name.startswith(prefix),
        vnc._objects_list(
            res_type="logical-router",
            detail=True,
        ),
    )

    filtered_vn = filter(
        lambda vn: vn.name.startswith(prefix),
        vnc._objects_list(
            res_type="virtual-network",
            detail=True,
        ),
    )

    target_vn_list: list[vnc_api.VirtualNetwork] = []
    target_vn_list.extend(filtered_vn)

    for lr in fitlered_lr:

        virtual_network_refs = lr.get_virtual_network_refs()
        if virtual_network_refs is None:
            continue

        for vn_ref in lr.get_virtual_network_refs():
            if isinstance(vn_ref["attr"], vnc_api.LogicalRouterVirtualNetworkType):
                vn: vnc_api.VirtualNetwork = vnc._object_read(
                    "virtual-network", id=vn_ref["uuid"]
                )
                target_vn_list.append(vn)

    ri_list = []
    for vn in target_vn_list:
        parent_lr = vn.get_logical_router_back_refs() or []
        for ri_ref in vn.get_routing_instances():
            ri_list.append(
                RoutingInstanceDTO(
                    fq_name=":".join(ri_ref["to"]),
                    parent_lr=[":".join(ref["to"]) for ref in parent_lr],
                )
            )

    return ri_list
