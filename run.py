#!/usr/bin/env python3

import importlib
from argparse import ArgumentParser, Namespace

from src.openstack.provisioner import NovaProvisioner
from src.openstack.repo import VirtualMachinesRepo
from src.patch_requests import monkey_patch_requests
from src.sdn.provisioner import SdnProvisioner
from src.sdn.repo import SdnReourcesRepo


def parse_cli() -> Namespace:
    arg_parser = ArgumentParser(description="Create/Delete/Find setup")

    arg_parser.add_argument(dest="setup_path", help="Path to setup code")
    arg_parser.add_argument(dest="command", choices=("create", "delete", "find"))
    arg_parser.add_argument(
        "-c",
        "--conf-file",
        dest="conf_file",
        required=True,
        help="Path to config file for stand",
    )
    arg_parser.add_argument(
        "-p",
        dest="monkey_patch_lvl",
        action="count",
        default=0,
        help="Patch requests. -p -- show POST data, -pp -- show POST data and response JSON",
    )

    args = arg_parser.parse_args()
    return args


def main():
    args = parse_cli()
    monkey_patch_requests(lvl=args.monkey_patch_lvl)

    command = args.command
    setup_path = args.setup_path
    if setup_path.startswith("./"):
        setup_path = setup_path[2:]
    setup_path = setup_path.split(".py")[0]
    module = setup_path.replace("/", ".")
    conf_file = args.conf_file

    setup = importlib.import_module(module)
    if "create_resources" not in setup.__dir__():
        raise Exception(f"In module '{module}' there is no function 'create_resources'")

    sdn_repo = SdnReourcesRepo()
    vm_repo = VirtualMachinesRepo()
    sdn = SdnProvisioner(conf_file=conf_file)
    nova = NovaProvisioner(conf_file=conf_file)

    setup.create_resources(sdn_repo=sdn_repo, vm_repo=vm_repo)

    if command == "create":
        sdn.provision(repo=sdn_repo)
        nova.provision(repo=vm_repo)
    elif command == "delete":
        sdn.erase(repo=sdn_repo)
        nova.erase(repo=vm_repo)
    elif command == "find":
        sdn.find(repo=sdn_repo)
        nova.find(repo=vm_repo)
    else:
        raise Exception(f"Don't know command '{command}")

    sdn_repo.show_list()
    vm_repo.show_list()


if __name__ == "__main__":
    main()
