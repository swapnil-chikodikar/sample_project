# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
# from sample_app import file_handler
from sla_scripts import vm_scaling
# import obj_main

obj = vm_scaling.VCenterconnection()

def welcome_page(request):
    return render(request, 'sample_app/welcome.html')


def vcenter_creds_form(request):
    return render(request, 'sample_app/vcenter_creds.html')


def vcenter_creds(request):
    hostname = request.POST['vcenter_ip']
    username = request.POST['username']
    password = request.POST['password']
    # obj_main.vcenter_login(hostname, username, password)
    obj.connect_to_vcenter(hostname, username, password)
    print(dir(obj))
    msg1 = "Success"
    # msg2 = obj.conn.msg1
    # return HttpResponse(msg1)
    return render(request, 'sample_app/deployment.html')

# def vcenter_creds(request):
#     hostname = request.POST['vcenter_ip']
#     username = request.POST['username']
#     password = request.POST['password']
#     obj = vm_scaling.VCenterconnection(hostname, username, password)
#     print(dir(obj))
#     msg1 = "Success"
#     # msg2 = obj.conn.msg1
#     return HttpResponse(msg1)
    # if obj.flag is not 1:
    #     msg = obj.conn
    #     return HttpResponse(msg)
    # else:
    #     return render(request, 'sample_app/scale_vm.html')


def deployment_page_form(request):
    return render(request, 'sample_app/deployment.html')

def vm_deployment(request):
    esx_host = request.POST['esx_host']
    dc_name = request.POST['dc_name']
    ds_name = request.POST['ds_name']
    temp_name = request.POST['temp_name']
    new_vm = request.POST['new_vm']
    obj.scale_vm(esx_host, dc_name, ds_name, temp_name, new_vm)
