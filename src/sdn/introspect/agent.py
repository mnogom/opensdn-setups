import xml.etree.ElementTree as ET

import requests


def find_link_local_ip(compute_node_ip: str, vm_uuid: str):
    response = requests.get(f"http://{compute_node_ip}:8085/Snh_ItfReq")
    root = ET.fromstring(response.text)

    for child in root.findall(".//ItfSandeshData"):
        if child.find("vmi_type").text != "Virtual Machine":
            continue

        if child.find("vm_uuid").text == vm_uuid:
            return child.find("mdata_ip_addr").text
