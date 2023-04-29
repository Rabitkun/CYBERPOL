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