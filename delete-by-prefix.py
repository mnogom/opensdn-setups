#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace

from src.openstack.provisioner import NovaProvisioner
from src.openstack.repo import VirtualMachinesRepo
from src.sdn.provisioner import ORDER_TO_PROVISION, SdnProvisioner
from src.sdn.repo import SdnReourcesRepo


def parse_cli() -> Namespace:
    arg_parser = ArgumentParser(description="Create resources by prefix")
    arg_parser.add_argument(dest="prefix", help="Resources prefix")
    arg_parser.add_argument(
        dest="type_source",
        choices=("all", "sdn", "nova"),
        default="all",
        nargs="?",
        help="Source of resource (all/sdn/nova). Default is 'all'",
    )
    arg_parser.add_argument(
        "-c",
        "--conf-file",
        dest="conf_file",
        required=True,
        help="Path to config file for stand",
    )
    return arg_parser.parse_args()


def clean_sdn_resources(sdn: SdnProvisioner, prefix: str):
    repo = SdnReourcesRepo()

    order_to_delete = ORDER_TO_PROVISION[::-1]
    for type_ in order_to_delete:
        resource_list = sdn._vnc._objects_list(
            res_type=type_,
            detail=True,
        )
        for res in resource_list:
            if res.name.startswith(prefix):
                repo._list.append(res)

    if len(repo._list) == 0:
        print("Nothing to delete in SDN")
        return

    repo.show_list()

    ans = input("delete all? (y/[n]) ")
    if ans == "y":
        sdn.erase(repo=repo)


def clean_nova_resources(nova: NovaProvisioner, prefix: str):
    repo = VirtualMachinesRepo()

    virtual_machine_list = nova._nova_api.list_virtual_machine(name=prefix)
    for virtual_machine in virtual_machine_list:
        repo._list.append(virtual_machine)

    if len(virtual_machine_list) == 0:
        print("Nothing to delete in Nova")
        return

    repo.show_list()

    ans = input("delete all? (y/[n]) ")
    if ans == "y":
        nova.erase(repo=repo)


if __name__ == "__main__":
    args = parse_cli()
    sdn = SdnProvisioner(conf_file=args.conf_file)
    nova = NovaProvisioner(conf_file=args.conf_file)

    prefix = args.prefix
    type_source = args.type_source
    if type_source in ("all", "sdn"):
        clean_sdn_resources(sdn, prefix=prefix)
    if type_source in ("all", "nova"):
        clean_nova_resources(nova, prefix=prefix)
