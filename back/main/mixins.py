from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.template.loader import render_to_string


def _get_menu_context():
    """
    Данные необходимые на каждой странице, например для рендеринга меню и
    блока авторизации
    """
    return {
    }


def login_page_view(request):
    # @TODO сейчас нет страницы логина
    context = _get_menu_context()
    response = HttpResponse(
        render_to_string('pages/index/login.pug', context, request),
        status=401,
    )
    response['Cache-Control'] = 'private, max-age=180'
    return response


class MenuContextMixin:
    def get_context_data(self, **kwargs):
        context = super(MenuContextMixin, self).get_context_data(**kwargs)
        context.update(_get_menu_context())
        return context


class LoginRequiredNoRedirectMixin(MenuContextMixin, AccessMixin):
    """
    LoginRequired, но без редиректа.
    Анонимным юзерам показывает пустой лэйаут с попапом логина.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return login_page_view(request)
        return super().dispatch(request, *args, **kwargs)
