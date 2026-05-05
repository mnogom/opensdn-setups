from pydantic.dataclasses import dataclass
from pydantic_xml import BaseXmlModel, element, wrapped
from rich.console import Console


class DictMixin:
    def dict(self):
        dict_ = {}
        for slot in self.__slots__:
            dict_[slot] = getattr(self, slot)
        return dict_


@dataclass(slots=True, frozen=True)
class ShowRouteReq(DictMixin):
    routing_table: str = ""
    routing_instance: str = ""
    prefix: str = ""
    longer_match: str = ""
    shorter_match: str = ""
    count: str = ""
    start_routing_table: str = ""
    start_routing_instance: str = ""
    start_prefix: str = ""
    source: str = ""
    protocol: str = ""
    family: str = ""


@dataclass(slots=True, frozen=True)
class ShowRoutingInstanceSummaryReq(DictMixin):
    search_string: str = ""


# ====================


class BaseContrailXmlModel(BaseXmlModel):
    __xml_search_mode__ = "unordered"


# ====================


class ShowRoutingInstance(BaseContrailXmlModel, tag="ShowRoutingInstance"):
    name: str = element()
    virtual_network: str = element()
    vn_index: int = element()
    vxlan_id: int = element()

    import_targets: list[str] = wrapped("import_target/list", element(tag="element"))
    export_targets: list[str] = wrapped("export_target/list", element(tag="element"))

    always_subscribe: bool = element()
    allow_transit: bool = element()
    pbb_evpn_enable: bool = element()
    deleted: bool = element()
    deleted_at: str | None = element(default=None)


class ShowRoutingInstanceSummaryResp(
    BaseContrailXmlModel, tag="ShowRoutingInstanceSummaryResp"
):
    # NOTE: Not full spec

    instances: list[ShowRoutingInstance] = wrapped(
        "instances/list", element(tag="ShowRoutingInstance", default_factory=list)
    )
    more: bool = element()


# ==================


class ShowPmsiTunnel(BaseContrailXmlModel, tag="ShowPmsiTunnel"):
    tunnel_type: str | None = element(tag="type", default=None)
    ar_type: str | None = element(default=None)
    identifier: str | None = element(default=None)
    label: int | None = element(default=None)
    flags: list[str] = wrapped(
        "flags/list", element(tag="element"), default_factory=list
    )


class ShowRoutePath(BaseContrailXmlModel, tag="ShowRoutePath"):
    protocol: str = element(default="")
    last_modified: str = element(default="")
    local_preference: int = element(default=0)
    med: int = element(default=0)
    local_as: int = element(default=0)
    peer_as: int = element(default=0)
    peer_router_id: str = element(default="")
    source: str = element(default="")
    as_path: str = element(default="")
    as4_path: str = element(default="")
    next_hop: str = element(default="")
    label: str = element(default="")
    origin: str = element(default="")
    replicated: bool = element(default=False)
    primary_table: str = element(default="")
    secondary_tables: list[str] = wrapped(
        "secondary_tables/list", element(tag="element"), default_factory=list
    )
    communities: list[str] = wrapped(
        "communities/list", element(tag="element", default_factory=list)
    )
    origin_vn: str | None = element(default=None)
    flags: list[str] = wrapped(
        "flags/list", element(tag="element"), default_factory=list
    )
    tunnel_encap: list[str] = wrapped(
        "tunnel_encap/list", element(tag="element", default_factory=list)
    )
    sequence_no: str | None = element(default=None)
    origin_vn_path: list[str] = wrapped(
        "origin_vn_path/list", element(tag="element", default_factory=list)
    )
    pmsi_tunnel: ShowPmsiTunnel | None = wrapped("pmsi_tunnel", element(default=None))


class ShowRoute(BaseContrailXmlModel, tag="ShowRoute"):
    prefix: str = element()
    last_modified: str = element()
    paths: list[ShowRoutePath] = wrapped("paths/list", element(default_factory=list))


class ShowRouteTable(BaseContrailXmlModel, tag="ShowRouteTable"):
    routing_instance: str = element()
    routing_table_name: str = element()

    deleted: bool | None = element(default=None)
    deleted_at: str | None = element(default=None)

    prefixes: int = element(default=0)
    paths: int = element(default=0)
    primary_paths: int = element(default=0)
    secondary_paths: int = element(default=0)
    infeasible_paths: int = element(default=0)
    stale_paths: int = element(default=0)
    llgr_stale_paths: int = element(default=0)

    routes: list[ShowRoute] = wrapped("routes/list", element(default_factory=list))


class ShowRouteResp(BaseContrailXmlModel, tag="ShowRouteResp"):
    # NOTE: Not full spec

    tables: list[ShowRouteTable] = wrapped("tables/list", element(default_factory=list))
