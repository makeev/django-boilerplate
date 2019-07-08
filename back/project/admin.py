import logging

from functools import partial
from boolean_switch.admin import AdminBooleanMixin

from constance.admin import Config, ConstanceAdmin
from django_cron.admin import CronJobLog, CronJobLogAdmin
from logentry_admin.admin import LogEntryAdmin
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib.admin import AdminSite, ModelAdmin, register
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from main.models import OTPDevice, OTPStaticCode, User

logger = logging.getLogger(__name__)


class CustomizedAdminSite(AdminSite):
    site_header = 'WebSite'
    site_title = 'WebSite'
    index_title = 'Admin'
    empty_value_display = '¯\\_(ツ)_/¯'

    def index(self, request, extra_context=None):
        """
        Можно просунуть дополнительный контент для главной страницы админки
        """
        if extra_context is None:
            extra_context = {}

        extra_context.update({
            # 'stats': stats,
        })

        return super(CustomizedAdminSite, self).index(request, extra_context)

    def get_urls(self):
        """
        Кастомные немодельные админские страницы нужно добавлять вот таким образом
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


class CustomUserAdmin(AdminImageMixin, AdminBooleanMixin, UserAdmin):
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
        Кастомный контекст для страницы редактирования
        """
        extra_context = extra_context or {}
        # user = User.objects.get(id=object_id)
        # extra_context['subscription_link'] = reverse(
        #     'main:manage_subscription', kwargs={'subscription_code': user.subscription_code}
        # )
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def has_import_permission(self, request):
        return False


class OTPDeviceAdmin(ModelAdmin):
    model = OTPDevice
    list_display = ['user', 'is_confirmed', 'is_active', 'created_at']
    readonly_fields = ['user', 'name', 'is_confirmed']
    search_fields = ['user__username']
    exclude = ['secret']
    actions_on_top = False
    actions_on_bottom = False
    actions = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OTPStaticCodeAdmin(ModelAdmin):
    model = OTPStaticCode
    list_display = ['user', 'used_code', 'used_at', 'is_active', 'created_at']
    readonly_fields = ['user']
    search_fields = ['user__username']
    actions_on_top = False
    actions_on_bottom = False
    actions = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(OTPDevice, OTPDeviceAdmin)
custom_admin_site.register(OTPStaticCode, OTPStaticCodeAdmin)
custom_admin_site.register(Group, GroupAdmin)
custom_admin_site.register(LogEntry, LogEntryAdmin)
custom_admin_site.register([Config], ConstanceAdmin)
custom_admin_site.register(CronJobLog, CronJobLogAdmin)
