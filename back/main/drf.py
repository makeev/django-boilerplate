from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import set_rollback
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import encoders
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from main.exceptions import ReadableException


def exception_handler(exc, context):
    """
    ReadableException handler added
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    if isinstance(exc, ReadableException):
        data = {'message': exc.detail, 'code': exc.code}
        if hasattr(exc, 'extra_kwargs'):
            data.update(exc.extra_kwargs)

        set_rollback()
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return None


def full_details_exception_handler(exc, context):
    """
    This overrides the default exception handler to
    include the human-readable message AND the error code
    so that clients can respond programmatically.
    """
    if isinstance(exc, APIException):
        exc.detail = exc.get_full_details()

    return exception_handler(exc, context)


class CustomJsonEncoder(encoders.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, Money):
        #     return {'amount': str(obj.amount), 'currency': obj.currency.code}
        return super(CustomJsonEncoder, self).default(obj)


class CustomJSONRenderer(JSONRenderer):
    encoder_class = CustomJsonEncoder
