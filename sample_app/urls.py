from django.conf.urls import url
from sample_app import views


urlpatterns = [
    url(r'VCenterCredsForm/', views.vcenter_creds_form),
    url(r'^vcenter_creds/$', views.vcenter_creds),
    url(r'^DeploymentForm/$', views.deployment_page_form),
    url(r'^deployment/$', views.vm_deployment),
    url(r'^$', views.welcome_page),
    url(r'^VmDeleteForm/$', views.vm_delete_form),
    url(r'^deleteVm/$', views.vm_delete),
    url(r'^AssignIPForm/$', views.assign_ips_form),
    url(r'^assignIP/$', views.assign_ips),
    url(r'^AddNicForm/$', views.add_nic_form),
    url(r'^add_nic/$', views.add_nic),

]
