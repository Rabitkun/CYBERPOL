import subprocess
from subprocess import CompletedProcess
from enum import Enum
import xml.etree.ElementTree as ET
import uuid
import random
import string

class NodeType(Enum):
    CLOUD = 1
    VM = 2

def clone_vm(reference_domain: str, new_domain: str) -> tuple[str, CompletedProcess]:
    new_domain = create_valid_name(new_domain)
    command = f"virt-clone --original {reference_domain} --name {new_domain} --auto-clone --check all=off"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return (new_domain, result)

def delete_vm(domain: str) -> CompletedProcess:
    command = f"virsh undefine --nvram {domain} --remove-all-storage"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def start_vm(domain: str) -> CompletedProcess:
    command = f"virsh start {domain}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def shutdown_vm(domain: str) -> CompletedProcess:
    command = f"virsh shutdown {domain}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def forceoff_vm(domain: str) -> CompletedProcess:
    command = f"virsh destroy {domain}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def get_vm_status(domain: str) -> str:
    command = f"virsh domstate {domain}"
    output = subprocess.check_output(command, shell=True)
    status = output.decode().strip()
    return status

def check_vm_exists(domain: str) -> bool:
    command = ['virsh', 'dominfo', domain]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return False
    return True

def create_valid_name(domain: str) -> str:
    new_domain = domain
    if check_vm_exists(new_domain) != True:
        return new_domain
    
    new_domain = f'{domain}-{1}'
    counter = 2
    while check_vm_exists(new_domain):
        new_domain = f'{domain}-{counter}'
        counter += 1

    return new_domain

def set_vnc_port(domain: str, port: int) -> tuple[int, CompletedProcess]:
    file_path = f"/etc/libvirt/qemu/{domain}.xml"
    tree = ET.parse(file_path)
    root = tree.getroot()
    root = root.find("devices")
    root = root.find("graphics")
    root.attrib["type"] = 'vnc'
    root.attrib["autoport"] = "no"
    root.attrib["port"] = str(port)
    tree.write(file_path)
    command = f"virsh define {file_path}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return (port, result)

def get_interface_count(domain: str) -> int:
    command = f"virsh domiflist {domain}"
    result = subprocess.check_output(command)
    interface_count = len(result.strip().splitlines()) - 2 
    return interface_count

def generate_mac() -> str:
    #mac_address = ":".join(uuid.uuid4().hex[i:i+2] for i in range(0, 12, 2))
    random_uuid = uuid.uuid4()

    # Преобразование UUID в MAC-адрес
    mac_address = "52:54:00:{}:{}:{}".format(
        random_uuid.hex[:2],
        random_uuid.hex[2:4],
        random_uuid.hex[4:6]
    )
    # Если первый байт первого октета равен 1, изменяем его на 2
    if mac_address[0:2] == "52" and int(mac_address[3:5], 16) % 2 == 1:
        mac_address = "52:54:00:{}:{}:{}".format(
            hex(int(mac_address[3:5], 16) + 1)[2:].zfill(2),
            mac_address[6:8],
            mac_address[9:11]
        )
    return mac_address

def add_interface_to_vm(domain: str) -> tuple[tuple[str, str], CompletedProcess]:
    if_count = get_interface_count(domain)
    mac = generate_mac()
    alias = f"veth{if_count}"
    command = f"virsh attach-interface --domain {domain} --type network --source null --mac {mac} --alias {alias} --config --persistent"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return (mac, alias), result

def generate_network_name() -> str:
    characters = string.ascii_letters + string.digits
    name = ''.join(random.choice(characters) for i in range(14))
    return name

def create_network() -> tuple[str, CompletedProcess]:
    name = generate_network_name()
    file_path = f"/etc/libvirt/qemu/networks/{name}.xml"

    network = ET.Element("network")
    name_el = ET.SubElement(network, "name")
    name_el.text = name
    bridge = ET.SubElement(network, "bridge")
    bridge.set("name", name)
    bridge.set("stp", "on")
    bridge.set("delay", "0")
    domain = ET.SubElement(network, "domain")
    domain.set("name", name)
    tree = ET.ElementTree(network)
    tree.write(file_path)

    command = f"virsh net-define {file_path}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return name, result

def attach_network_to_domain_interface(domain: str, if_mac: str, net: str) -> CompletedProcess:
    vm_config_path = f'/etc/libvirt/qemu/{domain}.xml'
    tree = ET.parse(vm_config_path)
    root = tree.getroot()
    interface = root.find(f"./devices/interface/mac[@address='{if_mac}']/..")
    source = interface.find("source")
    source.set("network", net)
    tree.write(vm_config_path)
    command = f"virsh define {vm_config_path}"

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def detach_network_from_domain_interface(domain: str, if_mac: str) -> CompletedProcess:
    null_net = "null"
    result = attach_network_to_domain_interface(domain, if_mac, null_net)
    return result

def start_network(network: str) -> CompletedProcess:
    command = f"virsh net-start {network}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def stop_network(network: str) -> CompletedProcess:
    command = f"virsh net-destroy {network}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def remove_network(network: str) -> CompletedProcess:
    command = f"virsh net-undefine {network}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result