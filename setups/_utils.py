# root / root
# user / root

from typing import Callable


USER_DATA_MAIN = """\
#cloud-config
users:
  - name: root
    lock_passwd: false
    hashed_passwd: $6$rounds=4096$9mC3jk3GxO8JVjP7$GelxofDArKt0yyRAOUOHFa.88SoHfUdBa1jRhgB5hrRzXUvYuHEwKLYOIZaYgNqbfFDTlEOc.UGIfbC.3TlN//
  - name: user
    lock_passwd: false
    hashed_passwd: $6$rounds=4096$9mC3jk3GxO8JVjP7$GelxofDArKt0yyRAOUOHFa.88SoHfUdBa1jRhgB5hrRzXUvYuHEwKLYOIZaYgNqbfFDTlEOc.UGIfbC.3TlN//
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
ssh_pwauth: true
runcmd:
  - echo "HI!"
  - sed -i "s/deb.debian.org/mirror.yandex.ru/g" /etc/apt/mirrors/debian.list
  - sed -i "s/deb.debian.org/mirror.yandex.ru/g" /etc/apt/mirrors/debian-security.list
"""

USER_DATA_INTERFACE_PROXY = """\
#cloud-config
users:
  - name: root
    lock_passwd: false
    hashed_passwd: $6$rounds=4096$9mC3jk3GxO8JVjP7$GelxofDArKt0yyRAOUOHFa.88SoHfUdBa1jRhgB5hrRzXUvYuHEwKLYOIZaYgNqbfFDTlEOc.UGIfbC.3TlN//
  - name: user
    lock_passwd: false
    hashed_passwd: $6$rounds=4096$9mC3jk3GxO8JVjP7$GelxofDArKt0yyRAOUOHFa.88SoHfUdBa1jRhgB5hrRzXUvYuHEwKLYOIZaYgNqbfFDTlEOc.UGIfbC.3TlN//
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
ssh_pwauth: true
runcmd:
  - echo "HI!"
  - sed -i "s/deb.debian.org/mirror.yandex.ru/g" /etc/apt/mirrors/debian.list
  - sed -i "s/deb.debian.org/mirror.yandex.ru/g" /etc/apt/mirrors/debian-security.list
  - echo 1 > /proc/sys/net/ipv4/ip_forward
  - iptables -A FORWARD -i ens3 -o ens4 -j ACCEPT
  - iptables -A FORWARD -i ens4 -o ens3 -j ACCEPT
"""


PARENT = "default-domain:admin"


def get_fq_name_fn(prefix: str) -> Callable[[str, bool], str]:
    def fq_name(name: str, with_parent: bool = True) -> str:
        if with_parent is True:
            return f"{PARENT}:{prefix}{name}"
        return f"{prefix}{name}"

    return fq_name
