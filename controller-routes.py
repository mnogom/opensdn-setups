#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace

from rich.console import Console
from rich.table import Table

from src.sdn.api_utils import get_routing_instances
from src.sdn.introspect.controller.adapter import ControllerIntrospect
from src.sdn.vnc_api_gen import WrappedVncApi


def parse_cli() -> Namespace:
    arg_parser = ArgumentParser(description="Show routes from introspect")
    arg_parser.add_argument(
        "-c",
        "--conf-file",
        dest="conf_file",
        required=True,
        help="Path to config file for stand",
    )
    arg_parser.add_argument(dest="prefix", help="Resources prefix")
    arg_parser.add_argument(
        "-f",
        "--family",
        dest="family",
        default="",
        choices=(
            "enet",
            "ermvpn",
            "evpn",
            "inet",
            "inetvpn",
            "inet6",
            "l3vpn",
            "rtarget",
        ),
        help="family type",
    )
    arg_parser.add_argument(
        "-i",
        "--controller-id",
        dest="controller_id",
        default=0,
        type=int,
        help="Use it if you need get Rotues from specific controller. Default - 0",
    )
    arg_parser.add_argument(
        "-n",
        "--name-only",
        dest="name_only",
        default=False,
        action="store_true",
        help="Show only routing instances names",
    )

    return arg_parser.parse_args()


def find_and_render(
    conf_file: str,
    prefix: str,
    controller_id: int,
    family: str,
    name_only: bool,
):
    console = Console()

    vnc = WrappedVncApi(conf_file=conf_file)
    controller = ControllerIntrospect(conf_file=conf_file, controller_id=controller_id)

    ri_api_list = get_routing_instances(vnc=vnc, prefix=prefix)

    for ri_api in ri_api_list:
        lr_prefix = "|".join(lr for lr in ri_api.parent_lr)

        if name_only is True:
            console.print(f"[green bold] {lr_prefix} @ {ri_api.fq_name}")
            continue

        route_tables = controller.request_routes(
            routing_instance=ri_api.fq_name, family=family
        )
        for rt in route_tables.tables:
            rich_table = Table(
                title=f"[green bold] {lr_prefix}\n{rt.routing_table_name}"
            )
            rich_table.add_column("prefix", no_wrap=True)
            rich_table.add_column("protocol", no_wrap=True)
            rich_table.add_column("source", no_wrap=True)
            rich_table.add_column("next_hop", no_wrap=True)
            rich_table.add_column("label", no_wrap=True)
            rich_table.add_column("origin_vn", max_width=63)

            for route in rt.routes:
                for path in route.paths:
                    rich_table.add_row(
                        route.prefix,
                        path.protocol,
                        path.source,
                        path.next_hop,
                        path.label,
                        path.origin_vn,
                    )

            console.print(rich_table)


def main():
    args = parse_cli()
    find_and_render(
        conf_file=args.conf_file,
        prefix=args.prefix,
        family=args.family,
        controller_id=args.controller_id,
        name_only=args.name_only,
    )


if __name__ == "__main__":
    main()
