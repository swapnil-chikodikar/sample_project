from django.conf.urls import url
from sample_app import views


urlpatterns = [
    url(r'VCenterCredsForm/', views.vcenter_creds_form, name='sample_app-vcentercreds'),
    url(r'^vcenter_creds/$', views.vcenter_creds),
    url(r'ScaleVM/', views.scale_vm, name='sample_app-scalevm'),
    url(r'^$', views.welcome_page),
]
