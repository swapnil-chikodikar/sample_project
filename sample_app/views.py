# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
# from sample_app import file_handler
from sla_scripts import vm_scaling


def welcome_page(request):
    return render(request, 'sample_app/welcome.html')


def vcenter_creds_form(request):
    return render(request, 'sample_app/vcenter_creds.html')


def vcenter_creds(request):
    hostname = request.POST['vcenter_ip']
    username = request.POST['username']
    password = request.POST['password']
    obj = vm_scaling.VCenterconnection(hostname, username, password)
    print(dir(obj))
    msg1 = "Success"
    # msg2 = obj.conn.msg1
    return HttpResponse(msg1)
    # if obj.flag is not 1:
    #     msg = obj.conn
    #     return HttpResponse(msg)
    # else:
    #     return render(request, 'sample_app/scale_vm.html')

# def search(request):
#     if 'q' in request.GET:
#         message = 'You searched for: %r' % request.GET['q']
#     else:
#         message = 'You submitted an empty form.'
#     data = request.GET['q']
#     file_handler.file_writer(data)
#     return HttpResponse(message)


def scale_vm(request):
    return render(request, 'sample_app/scale_vm.html')
