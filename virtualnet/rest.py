import subprocess, os
from subprocess import CompletedProcess
from django.views.decorators.csrf import csrf_exempt
from . import models, kvm
from django.db.models import Q
from django.http import JsonResponse, HttpRequest
import json
import urllib.parse

@csrf_exempt
def get_references_list(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': "Only GET method required!"})
    refs = models.Reference.objects.all()
    response = {}
    for ref in refs:
        response[str(ref.pk)] = ref.title
    return JsonResponse(response)

@csrf_exempt
def get_icons_list(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': "Only GET method required!"})
    icon_path = "virtualnet/static/micons"
    filenames: list[str] = os.listdir(icon_path)
    response = {}
    for file in filenames:
        response[file] = file
    return JsonResponse(response)

@csrf_exempt
def get_vms_list(request: HttpRequest):
    vms = models.VirtualMachine.objects.all()
    resp = {}
    for vm in vms:
        resp[vm.pk] = {
            "node": vm.node.pk,
            "domain": vm.domain,
            "reference": vm.reference.domain
        }
    return JsonResponse(resp)

@csrf_exempt
def get_node_params(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': "Only GET method required!"})
    node_id = int(request.GET["id"])
    node = models.Node.objects.get(pk=node_id)
    response = {
        "id": node_id,
        "title": node.title,
        "type": node.type,
        "type-text": models.NodeType(node.type).name,
        "lab": node.lab.pk,
        "lab-title": node.lab.title,
    }
    if(node.type == models.NodeType.VIRTUALMACHINE):
        vm = models.VirtualMachine.objects.get(node=node)
        response["vm_id"] = vm.pk
        response["reference"] = vm.reference.domain
        response["cpus"] = vm.cpus
        response["ram"] = vm.ramMB
        response["interfaces"] = vm.interfaces

    return JsonResponse(response)

@csrf_exempt
def create_cloud_node(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)
    lab_id = int(request.COOKIES['lab_id'])
    pos_x = int(json_params["pos_x"])
    pox_y = int(json_params["pos_y"])
    title = json_params["title"]

    lab = models.Lab.objects.get(pk=lab_id)
    node = models.Node()
    node.lab = lab
    node.posX, node.posY = pos_x, pox_y
    node.title = title
    node.iconPath = "cloud-svgrepo-com.svg"
    node.type = models.NodeType.CLOUD
    node.save()
    return JsonResponse({'status': 'success', 'message': f'Cloud {title} has been created with node-id {node.id} in lab {lab.title}'})

@csrf_exempt
def remove_cloud_node(request: HttpRequest):
    if request.method != "DELETE":
        return JsonResponse({'status': 'error', 'message': "Only DELETE method required!"})
    json_params = json.loads(request.body)
    node_id = int(json_params["id"])
    node = models.Node.objects.get(pk=node_id)
    lab = node.lab
    bridges = models.Bridge.objects.filter(Q(nodeA=node) | Q(nodeB=node))
    vm = models.VirtualMachine.objects.filter(node=node)

    if bridges.count() != 0:
        return JsonResponse({'status': 'error', 'message': "Delete BRIDGES!"})
    if node.type != models.NodeType.CLOUD:
        return JsonResponse({'status': 'error', 'message': "NOT CLOUD!"})

    print("!!! ДОБАВИТЬ УДАЛЕНИЕ БРИДЖЕЙ С ВИРТУАЛКАМИ !!!")

    node.delete()
    return JsonResponse({'status': 'success', 'message': f'Cloud {node_id}:{node.title} deleted from lab {lab.title}'})

@csrf_exempt
def create_vm_by_ref(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)
    
    lab_id = int(request.COOKIES['lab_id'])
    ref_id = int(json_params["reference"])
    new_domain = json_params["title"]
    pos_x = int(json_params["pos_x"])
    pos_y = int(json_params["pos_y"])
    icon = json_params["icon"]
    cpus = int(json_params["cpus"])
    ram = int(json_params["ram"])
    interfaces = int(json_params["interfaces"])

    lab = models.Lab.objects.get(pk=lab_id)
    reference = models.Reference.objects.get(pk=ref_id)
    
    # Выполнение команды клонирования виртуальной машины
    vm_domain, result = kvm.clone_vm(reference.domain, new_domain)

    if result.returncode == 0:
        node = models.Node(title=new_domain, lab=lab, type=models.NodeType.VIRTUALMACHINE)
        node.posX = pos_x
        node.posY = pos_y
        node.iconPath = icon
        node.save()
        vm = models.VirtualMachine(node=node, domain=vm_domain, reference=reference, isExist=True)
        vm.cpus = cpus
        vm.ramMB = ram
        vm.interfaces = interfaces
        vm.save()
        # Если клонирование прошло успешно, вернуть статус 200 и сообщение об успешном клонировании
        return JsonResponse({'status': 'success', 'message': f'VM {reference.domain} has been cloned to {vm_domain} in lab {lab.title}', "id": node.id})
    else:
        # Если произошла ошибка при клонировании, вернуть статус 500 и сообщение об ошибке
        return JsonResponse({'status': 'error', 'message': result.stderr.decode()})

@csrf_exempt   
def delete_vm(request: HttpRequest):
    if request.method != "DELETE":
        return JsonResponse({'status': 'error', 'message': "Only DELETE method required!"})
    json_params = json.loads(request.body)
    vm_id = int(json_params["id"])
    vm = models.VirtualMachine.objects.get(pk=vm_id)
    bridges = models.Bridge.objects.filter(Q(nodeA=vm.node) | Q(nodeB=vm.node))

    if bridges.count() != 0:
        return JsonResponse({'status': 'error', 'message': "Delete BRIDGES!"})
    print("!!! ДОБАВИТЬ УДАЛЕНИЕ БРИДЖЕЙ С ВИРТУАЛКАМИ !!!")

    result = kvm.delete_vm(vm.domain)
    print(result)
    if result.returncode == 0:
        vm.node.delete()
        # Если удаление прошло успешно, вернуть статус 200 и сообщение об успешном удалении
        return JsonResponse({'status': 'success', 'message': f'VM {vm.domain} has been undefined'})
    else:
        # Если произошла ошибка при удалении, вернуть статус 500 и сообщение об ошибке
        return JsonResponse({'status': 'error', 'message': result.stderr.decode()})
    
@csrf_exempt   
def get_vm_status(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': "Only GET method required!"})

    vm_id = int(request.GET["id"])
    vm = models.VirtualMachine.objects.get(pk=vm_id)
    result = kvm.get_vm_status(vm.domain)
    print(result)
    return JsonResponse({'id': vm.pk, 'domain': vm.domain, "status": result})

@csrf_exempt   
def start_vm(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)
    vm_id = int(json_params["id"])

    vm = models.VirtualMachine.objects.get(pk=vm_id)
    result = kvm.start_vm(vm.domain)
    print(result)
    if result.returncode == 0:
        return JsonResponse({'status': 'success', 'message': f'VM {vm.domain} has been started'})
    else:
        return JsonResponse({'status': 'error', 'message': result.stderr.decode()})
    
@csrf_exempt   
def shutdown_vm(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)
    vm_id = int(json_params["id"])

    vm = models.VirtualMachine.objects.get(pk=vm_id)
    result = kvm.shutdown_vm(vm.domain)
    print(result)
    if result.returncode == 0:
        return JsonResponse({'status': 'success', 'message': f'VM {vm.domain} has been shutdown'})
    else:
        return JsonResponse({'status': 'error', 'message': result.stderr.decode()})
    
@csrf_exempt   
def forceoff_vm(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)
    vm_id = int(json_params["id"])

    vm = models.VirtualMachine.objects.get(pk=vm_id)
    result = kvm.forceoff_vm(vm.domain)
    print(result)
    if result.returncode == 0:
        return JsonResponse({'status': 'success', 'message': f'VM {vm.domain} has been destroyed'})
    else:
        return JsonResponse({'status': 'error', 'message': result.stderr.decode()})
    
@csrf_exempt   
def set_vnc_port_vm(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    
    json_params = json.loads(request.body)
    vm_id = int(json_params["id"])
    vnc_port = int(json_params["port"])

    vm = models.VirtualMachine.objects.get(pk=vm_id)
    new_port, result = kvm.set_vnc_port(vm.domain, vnc_port)

    if result.returncode == 0:
        return JsonResponse({'status': 'success', 'message': f'VM {vm.domain} new VNC port {new_port}'})
    return JsonResponse({'status': 'error', 'message': result.stderr.decode()})
    
