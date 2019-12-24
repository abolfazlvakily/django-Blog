from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect


class Login(View):
    @staticmethod
    def get(request):
        form = AuthenticationForm()
        return render(request, 'auth/login.html', context={'form': form})

    @staticmethod
    def post(request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('article:article'))
            else:
                context = {
                    'error': _('username or password is not valid')
                }
                return render(request, 'auth/login.html', context)


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect(reverse('article:article'))
