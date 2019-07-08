from django.views.generic import TemplateView
from django.utils.translation import get_language

from main.mixins import MenuContextMixin
from news.models import Post
from project.helpers.cache_control_view import CacheMixin


class MockupView(MenuContextMixin, CacheMixin, TemplateView):
    pass


class HomepageView(MenuContextMixin, CacheMixin, TemplateView):
    template_name = 'index.html'

    cache_max_age = 60

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.published.all()
        return context
