from src.openstack.repo import VirtualMachinesRepo
from src.sdn import constants
from src.sdn.repo import SdnReourcesRepo
from setups._utils import USER_DATA_MAIN, USER_DATA_INTERFACE_PROXY, get_fq_name_fn

# .1  |           |            |
# .2  |           |            |
# *   |           |            |
# .5  |-(LR)------|            |
# *   |           |            |
# .10 |-(vm-1-10) |            |-(vm-3-10)
# .11 |           |-(vm-23-11)-|

PREFIX = "net-rt-mpls--"
fq_name = get_fq_name_fn(PREFIX)


def create_resources(sdn_repo: SdnReourcesRepo, vm_repo: VirtualMachinesRepo):
    nrt_10_10_12_0_24 = sdn_repo.create_route_table(
        fq_name=fq_name("nrt-10-10-12-0_24"),
        prefix_nh_tuples=[
            ("10.10.1.0/24", "10.10.3.11"),
            ("10.10.2.0/24", "10.10.3.11"),
        ],
    )
    nrt_10_10_3_0_24 = sdn_repo.create_route_table(
        fq_name=fq_name("nrt-10-10-3-0_24"),
        prefix_nh_tuples=[("10.10.3.0/24", "10.10.2.11")],
    )

    ipam = sdn_repo.create_ipam(fq_name=fq_name("ipam"))

    vn_1 = sdn_repo.create_virtual_network(
        fq_name=fq_name("vn-1"),
        cidr_list=["10.10.1.0/24"],
        ipam=ipam,
    )
    vn_2 = sdn_repo.create_virtual_network(
        fq_name=fq_name("vn-2"),
        cidr_list=["10.10.2.0/24"],
        ipam=ipam,
        route_table=nrt_10_10_3_0_24,
    )
    vn_3 = sdn_repo.create_virtual_network(
        fq_name=fq_name("vn-3"),
        cidr_list=["10.10.3.0/24"],
        ipam=ipam,
        route_table=nrt_10_10_12_0_24,
    )

    vmi_1_5 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-1-5"),
        virtual_network=vn_1,
        virtual_machine_interface_device_owner=constants.VMI_NETWORK_ROUTER_INTERFACE,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-1-5", with_parent=False),
        virtual_network=vn_1,
        virtual_machine_interface=vmi_1_5,
        instance_ip_address="10.10.1.5",
    )

    vmi_2_5 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-2-5"),
        virtual_network=vn_2,
        virtual_machine_interface_device_owner=constants.VMI_NETWORK_ROUTER_INTERFACE,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-2-5", with_parent=False),
        virtual_network=vn_2,
        virtual_machine_interface=vmi_2_5,
        instance_ip_address="10.10.2.5",
    )

    vmi_1_10 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-1-10"),
        virtual_network=vn_1,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-1-10", with_parent=False),
        virtual_network=vn_1,
        virtual_machine_interface=vmi_1_10,
        instance_ip_address="10.10.1.10",
    )

    vmi_2_11 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-2-11"),
        virtual_network=vn_2,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-2-11", with_parent=False),
        virtual_network=vn_2,
        virtual_machine_interface=vmi_2_11,
        instance_ip_address="10.10.2.11",
    )

    vmi_3_10 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-3-10"),
        virtual_network=vn_3,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-3-10", with_parent=False),
        virtual_network=vn_3,
        virtual_machine_interface=vmi_3_10,
        instance_ip_address="10.10.3.10",
    )

    vmi_3_11 = sdn_repo.create_virtual_machine_interface(
        fq_name=fq_name("vmi-3-11"),
        virtual_network=vn_3,
    )
    sdn_repo.create_instance_ip(
        name=fq_name("iip-3-11", with_parent=False),
        virtual_network=vn_3,
        virtual_machine_interface=vmi_3_11,
        instance_ip_address="10.10.3.11",
    )

    sdn_repo.create_logical_router(
        fq_name=fq_name("lr"),
        virtual_machine_interfaces=[
            vmi_1_5,
            vmi_2_5,
        ],
        logical_router_type=constants.LogicalRouterType.SNAT,
    )

    vm_repo.create_virtual_machine(
        name=fq_name("vm-1-10", with_parent=False),
        flavor_name="small",
        image_name="debian",
        availability_zone_id=0,
        network_vmi_tuples=[(vn_1, vmi_1_10)],
        user_data=USER_DATA_MAIN,
    )

    vm_repo.create_virtual_machine(
        name=fq_name("vm-23-11", with_parent=False),
        flavor_name="small",
        image_name="debian",
        availability_zone_id=0,
        network_vmi_tuples=[
            (vn_2, vmi_2_11),
            (vn_3, vmi_3_11),
        ],
        user_data=USER_DATA_INTERFACE_PROXY,
    )

    vm_repo.create_virtual_machine(
        name=fq_name("vm-3-10", with_parent=False),
        flavor_name="small",
        image_name="debian",
        availability_zone_id=0,
        network_vmi_tuples=[(vn_3, vmi_3_10)],
        user_data=USER_DATA_MAIN,
    )


# ./controller-routes.py -c configs/dev.ini net-rt-vxlan -f inet
