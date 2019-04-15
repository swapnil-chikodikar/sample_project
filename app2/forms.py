from django import forms
from django.contrib.auth.forms import AuthenticationForm


class VcenterLoginForm(AuthenticationForm):
    host_ip = forms.CharField(label='HOST IP')

    class Meta:
        fields = ['host_ip', 'username', 'password']
