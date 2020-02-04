from django.conf import settings
from django.conf.urls import url
from .views.pages import (
    HomepageView, MockupView
)


app_name = 'main'


urlpatterns = [
    url(r'^$', view=HomepageView.as_view(), name='home'),
]

if settings.DEBUG:
    # mock pages
    urlpatterns += [
        # url(r'^login-page/$', view=MockupView.as_view(template_name='pages/index/login-page.html')),
    ]
