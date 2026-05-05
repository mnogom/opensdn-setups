#!/usr/bin/env python3

import subprocess
from argparse import ArgumentParser, Namespace

from src.openstack.nova_api import NovaApi
from src.openstack.serial_console_client import create_cli_session
from src.sdn.introspect.agent import find_link_local_ip


def parse_cli() -> Namespace:
    arg_parser = ArgumentParser(description="Init console session")
    arg_parser.add_argument(
        "-c",
        "--conf-file",
        dest="conf_file",
        required=True,
        help="Path to config file for stand",
    )
    arg_parser.add_argument(
        dest="type",
        choices=("serial", "vnc", "ll"),
        help="Type of console: serial -- serial console; vnc -- vnc console (url); ll -- start ssh session via link local address. Make sure that hypervisor/vm has user 'user'",
    )
    arg_parser.add_argument(dest="uuid", help="ID of Virtual Machine")
    return arg_parser.parse_args()


def main():
    args = parse_cli()
    nova_api = NovaApi(conf_file=args.conf_file)
    vm = nova_api.get_virtual_machine(args.uuid)

    if args.type == "vnc":
        print(nova_api.get_vnc_console(vm))
        return
    if args.type == "serial":
        url = nova_api.get_serial_console(vm)
        print(url)

        ans = input("Do you wan't to connect? ([y]/n): ")
        if ans != "n":
            create_cli_session
        return

    if args.type == "ll":
        index = nova_api._availability_zones.index(vm.availability_zone)
        compute_node_ip = nova_api._compute_nodes[index]
        link_local_ip = find_link_local_ip(
            compute_node_ip=compute_node_ip,
            vm_uuid=vm.id,
        )
        subprocess.run(
            f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -J user@{compute_node_ip} user@{link_local_ip}".split()
        )

    else:
        raise Exception(f"Unknown console type '{args.type}")


if __name__ == "__main__":
    main()
