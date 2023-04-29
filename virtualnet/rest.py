import subprocess
from subprocess import CompletedProcess
from django.views.decorators.csrf import csrf_exempt
from . import models, kvm
from django.http import JsonResponse, HttpRequest
import json

@csrf_exempt
def get_vms_list(request: HttpRequest):
    vms = models.VirtualMachine.objects.all()
    resp = {}
    for vm in vms:
        resp[vm.pk] = {
            "domain": vm.domain,
            "reference": vm.reference.domain
        }
    return JsonResponse(resp)

@csrf_exempt
def create_vm_by_ref(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': "Only POST method required!"})
    json_params = json.loads(request.body)

    lab_id = int(json_params["lab_id"])
    ref_id = int(json_params["reference_id"])
    new_domain = json_params["new_domain"]
    icon_path = json_params["icon"]

    lab = models.Lab.objects.get(pk=lab_id)
    reference = models.Reference.objects.get(pk=ref_id)
    
    # Выполнение команды клонирования виртуальной машины
    result = kvm.clone_vm(reference.domain, new_domain)

    if result.returncode == 0:
        node = models.Node(title=new_domain, lab=lab)
        node.save()
        vm = models.VirtualMachine(node=node, domain=new_domain, reference=reference, isExist=True)
        vm.save()
        # Если клонирование прошло успешно, вернуть статус 200 и сообщение об успешном клонировании
        return JsonResponse({'status': 'success', 'message': f'VM {reference.domain} has been cloned to {new_domain} in lab {lab.title}'})
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