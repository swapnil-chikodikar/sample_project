# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sla_scripts import vm_scaling

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


def deployment_page_form(request):
    return render(request, 'sample_app/deployment.html')


def vm_deployment(request):
    esx_host = request.POST['esx_host']
    dc_name = request.POST['dc_name']
    ds_name = request.POST['ds_name']
    temp_name = request.POST['temp_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    new_vm = request.POST['new_vm']
    try:
        obj.scale_vm(esx_host, dc_name, ds_name, temp_name, s_range, e_range, new_vm)
        return redirect('sample_app/DeploymentForm/')
    except Exception as error:
        print(error.message)


def vm_delete_form(request):
    return render(request, 'sample_app/vm_delete.html')


def vm_delete(request):
    vm_name = request.POST['vm_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    try:
        obj.Multi_vm_delete(vm_name, s_range, e_range)
        return render(request, 'sample_app/VmDeleteForm/')
    except Exception as error:
        print(error.message)


def assign_ips_form(request):
    return render(request, 'sample_app/asign_ip.html')


def assign_ips(request):
    vm_name = request.POST['vm_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    try:
        obj.Multi_static_ips(vm_name, s_range, e_range)
        return render(request, 'sample_app/AssignIPForm/')
    except Exception as error:
        print(error.message)


def add_nic_form(request):
    return render(request, 'sample_app/add_nic.html')


def add_nic(request):
    vm_name = request.POST['vm_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    port_grp = request.POST['port_grp']
    try:
        for i in range(s_range, e_range):
            new_name = vm_name + "%s" % i
            obj.remove_nic(new_name)
            obj.add_nic(new_name, port_grp)

        return render(request, 'sample_app/AddNicForm/')
    except Exception as error:
        print(error.message)
