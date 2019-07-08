# coding: utf-8
#
from django.http import HttpResponse
from django.template.loader import render_to_string


def access_denied(request, exception=None):
    return HttpResponse(render_to_string('403.html', {}, request), status=403)


def page_not_found(request, exception=None):
    context = {
    }
    return HttpResponse(render_to_string('desktop/errors/404.mako', context, request), status=404)


def server_error(request, exception=None):
    return HttpResponse(render_to_string('500.html', {}, request), status=500)


def server_error_emulate(request, exception=None):
    return 1/0
