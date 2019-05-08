# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
    obj.connect_to_vcenter(hostname, username, password)
    return HttpResponseRedirect('/RTOSLAAutomation/VCenterCredsForm/')

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
    obj.scale_vm(esx_host, dc_name, ds_name, temp_name, s_range, e_range, new_vm)
    return HttpResponseRedirect('/RTOSLAAutomation/DeploymentForm/')


def vm_delete_form(request):
    return render(request, 'sample_app/vm_delete.html')


def vm_delete(request):
    vm_name = request.POST['vm_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    obj.Multi_vm_delete(vm_name, s_range, e_range)
    return HttpResponseRedirect('/RTOSLAAutomation/VmDeleteForm')


def assign_ips_form(request):
    return render(request, 'sample_app/assign_ip.html')


def assign_ips(request):
    vm_name = request.POST['vm_name']
    ip_addr = request.POST['ip_addr']
    subnet_mask = request.POST['subnet_mask']
    gateway = request.POST['gateway']
    dns1 = request.POST['dns1']
    dns2 = request.POST['dns2']
    dns_list = [dns1, dns2]
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    obj.Multi_static_ips(vm_name, ip_addr, s_range, e_range, subnet_mask, gateway, dns_list)
    return HttpResponseRedirect('/RTOSLAAutomation/AssignIPForm/')


def add_nic_form(request):
    return render(request, 'sample_app/add_nic.html')


def add_nic(request):
    vm_name = request.POST['vm_name']
    s_range = int(request.POST['s_range'])
    e_range = int(request.POST['e_range'])
    port_grp = request.POST['port_grp']
    for i in range(s_range, e_range):
        new_name = vm_name + "%s" % i
        obj.remove_nic(new_name)
        obj.add_nic(new_name, port_grp)
    return HttpResponseRedirect('/RTOSLAAutomation/AddNicForm/')

