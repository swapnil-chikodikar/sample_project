from sla_scripts import vm_scaling

obj = vm_scaling.VCenterconnection()


def vcenter_login(hostname, username, password):
    obj.connect_to_vcenter(hostname, username, password)
    msg = "Connection successfull"