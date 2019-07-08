from django.apps import apps
from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.views.defaults import server_error
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from project.admin import custom_admin_site
from django.views.static import serve
from django.contrib.staticfiles.views import serve as staticfiles_serve
from project.views import page_not_found, server_error_emulate, access_denied
from django_rq.urls import urlpatterns as urlpatterns_rq
from django.contrib.auth.decorators import user_passes_test
from decorator_include import decorator_include


app_name = 'project'

admin.site = custom_admin_site
admin.autodiscover()


urlpatterns = [
    # admin
    url(r'^admin/', include('boolean_switch.urls')),
    url(r'^admin/', admin.site.urls),

    # urls отдельных app'ов
    url(r'', include('main.urls', namespace='main')),
    url(r'', include('news.urls', namespace='news')),


    url(r'^admin/rq/', decorator_include(
        user_passes_test(lambda u: u.is_superuser),
        urlpatterns_rq
    )),

    # эмуляция ошибки (должно работать и без DEBUG)
    url(r'^500-e/$', server_error_emulate),

    # view для смены языка
    path('i18n/', include('django.conf.urls.i18n')),
]

# запись для media нужна для работы reverse
urlpatterns += [
    url(r'^(?P<path>favicon\.ico)$', staticfiles_serve, name='favicon'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]

# раздача статики
urlpatterns += staticfiles_urlpatterns()

# просмотр служебных страниц в режиме отладки
if settings.DEBUG:
    urlpatterns += [
        url(r'^403/$', access_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]

# if not settings.COLLECTED_STATIC:
#     urlpatterns += i18n_patterns(
#         url(r'^devtools/', include('devtools.urls', namespace='devtools')),
#         url(r'^jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
#     )


# обработчики служебных страниц
handler403 = 'project.views.access_denied'
handler404 = 'project.views.page_not_found'
handler500 = 'project.views.server_error'


# приличное имя для некоторых приложений
apps.get_app_config('main').verbose_name = 'Boilerplate Skeleton'
