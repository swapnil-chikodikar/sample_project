# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from app2.forms import VcenterLoginForm
from sla_scripts import vm_scaling


def vcenter_login_form(request):
    print("Step2")
    if request.method == 'POST':
        print("step3")
        form = VcenterLoginForm(request.POST)
        print("Step4")
        if form.is_valid():
            print("Step5")
            hostname = form.cleaned_data.get('host_ip')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            obj = vm_scaling.VCenterconnection(hostname, username, password)
            msg = obj.conn
            return HttpResponse(msg)
        else:
            msg = "Form not valid"
            return HttpResponse(msg)
        # hostname = request.POST['host_ip']
        # username = request.POST['username']
        # password = request.POST['password']
        # obj = vm_scaling.VCenterconnection(hostname, username, password)
        # msg = obj.conn
        # return HttpResponse(msg)
    else:
        print("step1")
        form = VcenterLoginForm()
        return render(request, 'app2/vcenter_login.html', {'form': form})
