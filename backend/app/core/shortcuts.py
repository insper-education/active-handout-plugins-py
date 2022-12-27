from django.shortcuts import redirect as django_redirect
from django.http.response import HttpResponseRedirectBase


def redirect(to, *args, **kwargs):
    if 'vscode' not in HttpResponseRedirectBase.allowed_schemes:
        HttpResponseRedirectBase.allowed_schemes.append('vscode')
    return django_redirect(to, *args, **kwargs)
