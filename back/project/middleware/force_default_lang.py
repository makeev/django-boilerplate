from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


DEFAULT_MAX_AGE = 0


class ForceDefaultLangMiddleware(MiddlewareMixin):
    """
    Установка языка из settings.LANGUAGE_CODE всегда, вместо HTTP_ACCEPT_LANGUAGE
    """

    def process_response(self, request, response):
        request.META['HTTP_ACCEPT_LANGUAGE'] = settings.LANGUAGE_CODE
        return response
