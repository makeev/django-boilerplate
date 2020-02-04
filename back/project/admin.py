import logging

from functools import partial

from constance.admin import Config, ConstanceAdmin
from logentry_admin.admin import LogEntryAdmin
from django.contrib.admin import AdminSite, ModelAdmin, register
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from main.models import User

logger = logging.getLogger(__name__)


class CustomizedAdminSite(AdminSite):
    site_header = 'WebSite'
    site_title = 'WebSite'
    index_title = 'Admin'
    empty_value_display = '¯\\_(ツ)_/¯'

    def index(self, request, extra_context=None):
        """
        Extra context for admin mainpage
        """
        if extra_context is None:
            extra_context = {}

        extra_context.update({
            # 'stats': stats,
        })

        return super(CustomizedAdminSite, self).index(request, extra_context)

    def get_urls(self):
        """
        Custom admin pages
        """
        urlpatterns = super().get_urls()
        # urlpatterns += [
        #     url(r'^user/toggle/$',
        #         self.admin_view(toggle_view),
        #         name='user_toggle_view'
        #     ),
        # ]
        return urlpatterns


custom_admin_site = CustomizedAdminSite()
admin_register = partial(register, site=custom_admin_site)


class CustomUserAdmin(UserAdmin):
    # change_form_template = 'admin/user_change_view.html'

    model = User
    list_display = ['_username', 'first_name', 'last_name', 'is_staff',
                    'is_superuser', 'is_active']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email', '=id')
    list_per_page = 100
    ordering = ['-id']

    def _username(self, obj):
        if isinstance(obj.username, str):
            return obj.username.lower()
        return obj.username

    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'is_email_verified')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'password_changed_at')}),
    )
    actions_on_top = False
    actions_on_bottom = False
    actions = None

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Custom change view
        """
        extra_context = extra_context or {}
        # user = User.objects.get(id=object_id)
        # extra_context['subscription_link'] = reverse(
        #     'main:manage_subscription', kwargs={'subscription_code': user.subscription_code}
        # )
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def has_import_permission(self, request):
        return False


custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(Group, GroupAdmin)
custom_admin_site.register(LogEntry, LogEntryAdmin)
custom_admin_site.register([Config], ConstanceAdmin)
