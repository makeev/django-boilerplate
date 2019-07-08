from django.conf import settings
from project.admin import custom_admin_site
from constance import config


def each_context(request):
    """
    Контекст для корректного отображения кастомных страниц админки, которые сами не добавляют each_context.
    """
    # FIXME: обязательно сделать так, чтобы данный контекст собирался только для страниц внутри админки
    context = custom_admin_site.each_context(request)
    # context['CSRF_COOKIE_NAME'] = settings.CSRF_COOKIE_NAME
    # context['CSRF_COOKIE_PATH'] = settings.CSRF_COOKIE_PATH
    return context


def constance_context(request):
    conf_dict = {}
    for k in dir(config):
        conf_dict[k] = getattr(config, k)

    return {
        'CONSTANCE': conf_dict
    }
