import subprocess
from subprocess import CompletedProcess
from enum import Enum
import xml.etree.ElementTree as ET

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