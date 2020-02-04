from django.views.generic import TemplateView

from main.mixins import MenuContextMixin
from project.helpers.cache_control_view import CacheMixin


class MockupView(MenuContextMixin, CacheMixin, TemplateView):
    pass


class HomepageView(MenuContextMixin, CacheMixin, TemplateView):
    template_name = 'index.html'

    cache_max_age = 60

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
