import subprocess
from subprocess import CompletedProcess

def clone_vm(reference_domain: str, new_domain: str) -> CompletedProcess:
    command = f"virt-clone --original {reference_domain} --name {new_domain} --auto-clone --check all=off"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

def delete_vm(domain: str) -> CompletedProcess:
    command = f"virsh undefine --nvram {domain} --remove-all-storage"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result