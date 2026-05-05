# TLDR
```
make install
. .source
./run.py -c configs/example.ini setups/xx_int_rt_mpls.py create
./controller-routes.py -c configs/example.ini int-rt-mpls -f inet
./run.py -c configs/example.ini setups/xx_int_rt_mpls.py delete
```

# Install
```bash
make install
```

# Config file
look for `configs/exmample.ini` and replace ip addresses / ports of services

# CLI utils
## Main info
```bash
# Do
. .source
./run.py ...  # to run like this
# or use 'uv run'
uv run xxx.py ...
```

## `./run.py`
```bash
usage: run.py [-h] -c CONF_FILE [-p] setup_path {create,delete,find}

Create/Delete/Find setup

positional arguments:
  setup_path            Path to setup code
  {create,delete,find}

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file for stand
  -p                    Patch requests. -p -- show POST data, -pp -- show POST data and response JSON
```

## `./console.py`
```bash
usage: console.py [-h] -c CONF_FILE {serial,vnc,ll} uuid

Init console session

positional arguments:
  {serial,vnc,ll}       Type of console: serial -- serial console; vnc -- vnc console (url); ll -- start ssh session via link local address. Make sure that hypervisor/vm has user 'user'
  uuid                  ID of Virtual Machine

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file for stand
```

## `./delete-by-prefix.py`
```bash
usage: delete-by-prefix.py [-h] -c CONF_FILE prefix [{all,sdn,nova}]

Create resources by prefix

positional arguments:
  prefix                Resources prefix
  {all,sdn,nova}        Source of resource (all/sdn/nova). Default is 'all'

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file for stan
```

## `./delete-by-uuid`
```bash
usage: delete-by-uuid.py [-h] -c CONF_FILE {sdn,nova} uuid

Delete resource by uuid

positional arguments:
  {sdn,nova}            Source of resource (sdn/nova)
  uuid                  ID of Resource / Virtual Machine

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file for stand
```

## `./controller-routes.py`
```bash
usage: controller-routes.py [-h] -c CONF_FILE [-f {enet,ermvpn,evpn,inet,inetvpn,inet6,l3vpn,rtarget}] [-i CONTROLLER_ID] prefix

Show routes from introspect

positional arguments:
  prefix                Resources prefix

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf-file CONF_FILE
                        Path to config file for stand
  -f {enet,ermvpn,evpn,inet,inetvpn,inet6,l3vpn,rtarget}, --family {enet,ermvpn,evpn,inet,inetvpn,inet6,l3vpn,rtarget}
                        family type
  -i CONTROLLER_ID, --controller-id CONTROLLER_ID
                        Use it if you need get Rotues from specific controller. Default - 0
```


## Example:
```bash
root -> ./run.py -c configs/dev.ini setups/vni.py create
SDN Creating ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02
VM creating ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
                                                  SDN Reources
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ uuid                                 ┃ type                      ┃ fq_name                                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ a7563674-7074-4719-8716-fd1a6d01e789 │ network-ipam              │ default-domain:admin:vni-2001--ipam        │
│ 1d90d522-85ed-4702-94b3-6dd9e0132b51 │ virtual-network           │ default-domain:admin:vni-2001--vn-1        │
│ 17482f50-c024-4b52-8b97-5d6f7c296cbb │ virtual-network           │ default-domain:admin:vni-2001--vn-2        │
│ 7d791b1d-7238-4cc0-94a7-e53e9510215f │ security-group            │ default-domain:admin:vni-2001--sg          │
│ bf47bd35-e910-4f76-86f1-48ef15ba1104 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-lr-1-5  │
│ fdc19869-f214-42b5-a012-a3f10b715739 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-lr-2-5  │
│ 29313a0d-c433-485f-abb3-3adc6393dc0b │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-vm-1-10 │
│ 106e47ad-c716-49b0-a1ae-37d520cbdf12 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-vm-2-10 │
│ 935a4601-9051-4bc2-a7b9-d02da4449bb0 │ instance-ip               │ vni-2001--ip-lr-1-5                        │
│ d60c008b-1d91-4679-864b-01c56ffd310b │ instance-ip               │ vni-2001--ip-lr-2-5                        │
│ 5efd1993-a79c-4e1a-b7c3-c7365279391c │ instance-ip               │ vni-2001--ip-vm-1-10                       │
│ 98ba25bf-2a8a-4734-832c-281dc8364840 │ instance-ip               │ vni-2001--ip-vm-2-10                       │
│ ee04bb4b-2cce-47dd-bcb3-c4f3e27ea3b0 │ logical-router            │ default-domain:admin:vni-2001--lr          │
└──────────────────────────────────────┴───────────────────────────┴────────────────────────────────────────────┘
                                Virtual Machines
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ uuid                                 ┃ name              ┃ availability zone ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ 00bf5292-b16e-47f4-b75d-621344aa6bea │ vni-2001--vm-1-10 │ 0                 │
│ 0e9e8462-bedc-4700-aa74-bc46ff027033 │ vni-2001--vm-2-10 │ 1                 │
└──────────────────────────────────────┴───────────────────┴───────────────────┘

root -> ./controller-routes.py -c ./configs/dev.ini vni-2001 -f evpn

                                             default-domain:admin:vni-2001--vn-1:vni-2001--vn-1.evpn.0
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ prefix                                       ┃ protocol ┃ source                   ┃ next_hop     ┃ label ┃ origin_vn                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 2-0:0-30-02:29:31:3a:0d:c4,0.0.0.0           │ XMPP     │ cxsdn-1n5.cp.dev.cldx.ru │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 2-0:0-30-02:29:31:3a:0d:c4,0.0.0.0           │ BGP      │ 10.0.4.134               │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 2-0:0-30-02:29:31:3a:0d:c4,192.168.81.11     │ XMPP     │ cxsdn-1n5.cp.dev.cldx.ru │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 2-0:0-30-02:29:31:3a:0d:c4,192.168.81.11     │ BGP      │ 10.0.4.134               │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 2-10.0.1.135:57-30-ff:ff:ff:ff:ff:ff,0.0.0.0 │ XMPP     │ cxsdn-1n5.cp.dev.cldx.ru │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 3-10.40.184.20:57-30-10.40.184.20            │ Local    │                          │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 3-10.40.184.20:57-30-10.40.184.20            │ BGP      │ 10.0.4.134               │ 10.40.184.20 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 3-10.40.184.21:39-30-10.40.184.21            │ BGP      │ 10.0.1.246               │ 10.40.184.21 │ 30    │ default-domain:admin:vni-2001--vn-1 │
│ 3-10.40.184.21:39-30-10.40.184.21            │ BGP      │ 10.0.4.134               │ 10.40.184.21 │ 30    │ default-domain:admin:vni-2001--vn-1 │
└──────────────────────────────────────────────┴──────────┴──────────────────────────┴──────────────┴───────┴─────────────────────────────────────┘

                                             default-domain:admin:vni-2001--vn-2:vni-2001--vn-2.evpn.0
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ prefix                                       ┃ protocol ┃ source                   ┃ next_hop     ┃ label ┃ origin_vn                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 2-0:0-56-02:10:6e:47:ad:c7,0.0.0.0           │ XMPP     │ cxsdn-1n6.cp.dev.cldx.ru │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 2-0:0-56-02:10:6e:47:ad:c7,0.0.0.0           │ BGP      │ 10.0.1.246               │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 2-0:0-56-02:10:6e:47:ad:c7,192.168.82.11     │ XMPP     │ cxsdn-1n6.cp.dev.cldx.ru │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 2-0:0-56-02:10:6e:47:ad:c7,192.168.82.11     │ BGP      │ 10.0.1.246               │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 2-10.0.0.101:38-56-ff:ff:ff:ff:ff:ff,0.0.0.0 │ XMPP     │ cxsdn-1n6.cp.dev.cldx.ru │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 2-10.0.0.101:58-56-ff:ff:ff:ff:ff:ff,0.0.0.0 │ XMPP     │ cxsdn-1n5.cp.dev.cldx.ru │ 10.40.184.20 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 3-10.40.184.20:58-56-10.40.184.20            │ Local    │                          │ 10.40.184.20 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 3-10.40.184.20:58-56-10.40.184.20            │ BGP      │ 10.0.0.119               │ 10.40.184.20 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 3-10.40.184.21:38-56-10.40.184.21            │ Local    │                          │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
│ 3-10.40.184.21:38-56-10.40.184.21            │ BGP      │ 10.0.1.246               │ 10.40.184.21 │ 56    │ default-domain:admin:vni-2001--vn-2 │
└──────────────────────────────────────────────┴──────────┴──────────────────────────┴──────────────┴───────┴─────────────────────────────────────┘
                                                              default-domain:admin:vni-2001--lr
default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-47dd-bcb3-c4f3e27ea3b0__:__contrail_lr_internal_vn_ee04bb4b-2cce-47dd-bcb3-c4f3e27ea3b0__.evpn.
                                                                             0
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ prefix                    ┃ protocol ┃ source                   ┃ next_hop     ┃ label ┃ origin_vn                                                       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 5-0:0-0-0.0.0.0/0         │ BGP      │ 10.21.201.96             │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-0.0.0.0/0         │ BGP      │ 10.0.0.119               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-0.0.0.0/0         │ BGP      │ 10.0.4.150               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-10.20.90.0/24     │ BGP      │ 10.21.201.96             │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-10.20.90.0/24     │ BGP      │ 10.0.0.119               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-10.20.90.0/24     │ BGP      │ 10.0.4.150               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.81.11/32  │ BGP      │ 10.0.0.119               │ 10.40.184.20 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.81.11/32  │ BGP      │ 10.0.4.150               │ 10.40.184.20 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.82.11/32  │ XMPP     │ cxsdn-1n6.cp.dev.cldx.ru │ 10.40.184.21 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.82.11/32  │ BGP      │ 10.0.4.150               │ 10.40.184.21 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.255.95/32 │ BGP      │ 10.21.201.96             │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.255.95/32 │ BGP      │ 10.0.0.119               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
│ 5-0:0-0-192.168.255.95/32 │ BGP      │ 10.0.4.150               │ 10.21.201.95 │ 2001  │ default-domain:admin:__contrail_lr_internal_vn_ee04bb4b-2cce-4… │
└───────────────────────────┴──────────┴──────────────────────────┴──────────────┴───────┴─────────────────────────────────────────────────────────────────┘

root -> ./run.py -c configs/dev.ini setups/vni.py delete
SDN Deleting ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
VM deleting ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
                                                  SDN Reources
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ uuid                                 ┃ type                      ┃ fq_name                                    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ee04bb4b-2cce-47dd-bcb3-c4f3e27ea3b0 │ logical-router            │ default-domain:admin:vni-2001--lr          │
│ 935a4601-9051-4bc2-a7b9-d02da4449bb0 │ instance-ip               │ vni-2001--ip-lr-1-5                        │
│ d60c008b-1d91-4679-864b-01c56ffd310b │ instance-ip               │ vni-2001--ip-lr-2-5                        │
│ 5efd1993-a79c-4e1a-b7c3-c7365279391c │ instance-ip               │ vni-2001--ip-vm-1-10                       │
│ 98ba25bf-2a8a-4734-832c-281dc8364840 │ instance-ip               │ vni-2001--ip-vm-2-10                       │
│ bf47bd35-e910-4f76-86f1-48ef15ba1104 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-lr-1-5  │
│ fdc19869-f214-42b5-a012-a3f10b715739 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-lr-2-5  │
│ 29313a0d-c433-485f-abb3-3adc6393dc0b │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-vm-1-10 │
│ 106e47ad-c716-49b0-a1ae-37d520cbdf12 │ virtual-machine-interface │ default-domain:admin:vni-2001--vmi-vm-2-10 │
│ 7d791b1d-7238-4cc0-94a7-e53e9510215f │ security-group            │ default-domain:admin:vni-2001--sg          │
│ 1d90d522-85ed-4702-94b3-6dd9e0132b51 │ virtual-network           │ default-domain:admin:vni-2001--vn-1        │
│ 17482f50-c024-4b52-8b97-5d6f7c296cbb │ virtual-network           │ default-domain:admin:vni-2001--vn-2        │
│ a7563674-7074-4719-8716-fd1a6d01e789 │ network-ipam              │ default-domain:admin:vni-2001--ipam        │
└──────────────────────────────────────┴───────────────────────────┴────────────────────────────────────────────┘
                                Virtual Machines
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ uuid                                 ┃ name              ┃ availability zone ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ 00bf5292-b16e-47f4-b75d-621344aa6bea │ vni-2001--vm-1-10 │ 0                 │
│ 0e9e8462-bedc-4700-aa74-bc46ff027033 │ vni-2001--vm-2-10 │ 1                 │
└──────────────────────────────────────┴───────────────────┴───────────────────┘
```
