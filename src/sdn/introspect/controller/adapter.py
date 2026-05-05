import configparser
from enum import StrEnum

import requests

from src.sdn.introspect.controller.contracts import (
    ShowRouteReq,
    ShowRouteResp,
    ShowRoutingInstanceSummaryReq,
    ShowRoutingInstanceSummaryResp,
)


class IntrospectMethods(StrEnum):
    SHOW_ROUTING_INSTANCE_SUMMARY_REQ = "Snh_ShowRoutingInstanceSummaryReq"
    SHOW_ROUTE_REQ = "Snh_ShowRouteReq"


class ControllerIntrospect:
    def __init__(self, conf_file: str, controller_id: int):
        cfg_parser = configparser.ConfigParser(strict=False)
        cfg_parser.read(conf_file)

        self._hosts = cfg_parser.get("controller", "NODES").split(",")
        self._port = cfg_parser.get("controller", "INTROSPECT_PORT")
        self._controller_id = controller_id

    @property
    def _host(self) -> str:
        return self._hosts[self._controller_id]

    def _get_response(
        self,
        *,
        method: IntrospectMethods,
        query: ShowRouteReq | ShowRoutingInstanceSummaryReq,
    ):
        url = f"http://{self._host}:{self._port}/{method}"
        return requests.get(url=url, params=query.dict())

    def request_routes(
        self,
        *,
        routing_table: str = "",
        routing_instance: str = "",
        prefix: str = "",
        longer_match: str = "",
        shorter_match: str = "",
        count: str = "",
        start_routing_table: str = "",
        start_routing_instance: str = "",
        start_prefix: str = "",
        source: str = "",
        protocol: str = "",
        family: str = "",
    ) -> ShowRouteResp:
        response = self._get_response(
            method=IntrospectMethods.SHOW_ROUTE_REQ,
            query=ShowRouteReq(
                routing_table=routing_table,
                routing_instance=routing_instance,
                prefix=prefix,
                longer_match=longer_match,
                shorter_match=shorter_match,
                count=count,
                start_routing_table=start_routing_table,
                start_routing_instance=start_routing_instance,
                start_prefix=start_prefix,
                source=source,
                protocol=protocol,
                family=family,
            ),
        )

        res = ShowRouteResp.from_xml(response.text)
        return res

    def request_ri_summary(
        self,
        *,
        search_string: str = "",
    ) -> ShowRoutingInstanceSummaryResp:
        response = self._get_response(
            method=IntrospectMethods.SHOW_ROUTING_INSTANCE_SUMMARY_REQ,
            query=ShowRoutingInstanceSummaryReq(
                search_string=search_string,
            ),
        )
        return ShowRoutingInstanceSummaryResp.from_xml(response.text)
