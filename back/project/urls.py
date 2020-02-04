from django.apps import apps
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.defaults import server_error
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from project.admin import custom_admin_site
from django.views.static import serve
from django.contrib.staticfiles.views import serve as staticfiles_serve
from project.views import page_not_found, server_error_emulate, access_denied


app_name = 'project'

admin.site = custom_admin_site
admin.autodiscover()


urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),

    # urls for apps
    url(r'', include('main.urls', namespace='main')),


    # 500 error emulate for error reporting test
    url(r'^500-e/$', server_error_emulate),
]

# reverse for media
urlpatterns += [
    url(r'^(?P<path>favicon\.ico)$', staticfiles_serve, name='favicon'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]

# static patterns
urlpatterns += staticfiles_urlpatterns()

# debug pages
if settings.DEBUG:
    urlpatterns += [
        url(r'^403/$', access_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]


# custom error handlers
handler403 = 'project.views.access_denied'
handler404 = 'project.views.page_not_found'
handler500 = 'project.views.server_error'


# decent name for your project
apps.get_app_config('main').verbose_name = 'Project'
