from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


DEFAULT_MAX_AGE = 0


class ForceDefaultLangMiddleware(MiddlewareMixin):
    """
    Set language from settings.LANGUAGE_CODE always, instead of HTTP_ACCEPT_LANGUAGE
    """
    def process_response(self, request, response):
        request.META['HTTP_ACCEPT_LANGUAGE'] = settings.LANGUAGE_CODE
        return response
