from enum import StrEnum


class StrictStrEnum(StrEnum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return super().__repr__()


VMI_NETWORK_ROUTER_INTERFACE = "network:router_interface"

ALL_PORTS = [0, 65535]


class IPAMSubnetMethod(StrictStrEnum):
    USER_DEFINED_SUBNET = "user-defined-subnet"
    FLAT_SUBNET = "flat-subnet"
    AUTO_SUBNET = "auto-subnet"


class IPAMDNSMethod(StrictStrEnum):
    NONE = "none"
    DEFAULT_DNS_SERVER = "default-dns-server"
    TENANT_DNS_SERVER = "tenant-dns-server"
    VIRTAUL_DNS_SERVER = "virtual-dns-server"


class NetworkAddressAllocationMode(StrictStrEnum):
    USER_DEFINED_SUBNET_PREFERRED = "user-defined-subnet-preferred"
    USER_DEFINED_SUBNET_ONLY = "user-defined-subnet-only"
    FLAT_SUBNET_PREFERRED = "flat-subnet-preferred"
    FLAT_SUBNET_ONLY = "flat-subnet-only"


class LogicalRouterType(StrictStrEnum):
    VXLAN = "vxlan-routing"
    SNAT = "snat-routing"


class PolicyRuleDirection(StrictStrEnum):
    RIGHT = ">"
    LEFT_RIGHT = "<>"


class PolicyRuleProtocols(StrictStrEnum):
    ICMP = "icmp"
    ICMP6 = "icmp6"
    TCP = "tcp"
    UDP = "udp"
    ANY = "any"


class PolicyRuleEtherType(StrictStrEnum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class NextHopType(StrictStrEnum):
    SERVICE_INSTANCE = "service-instance"
    IP_ADDRESS = "ip-address"


class AllowAddressPairMode(StrictStrEnum):
    ACTIVE_ACTIVE = "active-active"
    ACTIVE_STANDBY = "active-standby"


ORDER_TO_PROVISION = [
    "network-ipam",
    "route-table",
    "virtual-network",
    "security-group",
    "interface-route-table",
    "virtual-machine-interface",
    "instance-ip",
    "logical-router",
]
