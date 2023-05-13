from django.shortcuts import render
import subprocess
from subprocess import CompletedProcess
from django.views.decorators.csrf import csrf_exempt
from . import models, kvm
from django.http import JsonResponse, HttpRequest
import json

# Create your views here.

def lab_field(request: HttpRequest):
    lab_id = int(request.COOKIES['lab_id'])
    lab = models.Lab.objects.get(pk=lab_id)
    nodes = models.Node.objects.filter(lab=lab)
    bridges = models.Bridge.getLabBridges(lab)
    for node in nodes:
        print(node.iconPath)
    print(bridges)
    return render(request, "lab/lab_base.html", {"lab_title": lab.title, "nodes": nodes, "bridges": bridges})