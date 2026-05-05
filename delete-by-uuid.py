#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace

from src.openstack.nova_api import NovaApi
from src.sdn.vnc_api_gen import WrappedVncApi


def parse_cli() -> Namespace:
    arg_parser = ArgumentParser(description="Delete resource by uuid")
    arg_parser.add_argument(
        "-c",
        "--conf-file",
        dest="conf_file",
        required=True,
        help="Path to config file for stand",
    )
    arg_parser.add_argument(
        dest="type_source",
        choices=("sdn", "nova"),
        help="Source of resource (sdn/nova)",
    )
    arg_parser.add_argument(dest="uuid", help="ID of Resource / Virtual Machine")
    return arg_parser.parse_args()


def remove_from_sdn(conf_file: str, uuid: str):
    vnc = WrappedVncApi(conf_file=conf_file)
    fq_name, type_ = vnc.id_to_fq_name_type(uuid)
    ans = input(f"Delete {type_}: {fq_name}? y/[n]: ")
    if ans == "y":
        vnc._object_delete(res_type=type_, fq_name=fq_name)


def remove_from_nova(conf_file: str, uuid: str):
    nova = NovaApi(conf_file=conf_file)
    vm = nova.get_virtual_machine(uuid)
    ans = input(f"Delete vm: {vm.name}? y/[n]: ")
    if ans == "y":
        nova.delete_virtual_machine(vm)


def main():
    args = parse_cli()
    conf_file = args.conf_file
    type_source = args.type_source
    if type_source == "sdn":
        remove_from_sdn(conf_file=conf_file, uuid=args.uuid)
    elif type_source == "nova":
        remove_from_nova(conf_file=conf_file, uuid=args.uuid)
    else:
        print(f"Unknown source type '{type_source}'")


if __name__ == "__main__":
    main()
