from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Login(forms.Form):
    username_field = forms.CharField(help_text=_(''))
