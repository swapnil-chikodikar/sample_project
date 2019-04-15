from django.conf.urls import url
from app2 import views as app2_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'vcenter_login', auth_views.LoginView.as_view(template_name='app2/vcenter_login.html'), name='VcenterLogin'),


]
