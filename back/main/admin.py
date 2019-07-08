import datetime
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from project.admin import custom_admin_site
from django.contrib.admin.filters import DateFieldListFilter
from django.db import models
from project.helpers.stuff import sizeof_fmt
from admin_comments.admin import CommentInline

from main.models import (
    MediaFile,
)


CommentInline.classes = []  # removing collapse class


class CustomDateFieldListFilter(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super(CustomDateFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        self.links = (
            (_('Any date'), {}),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Past 7 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=7)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(next_month),
            }),
            (_('This year'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(next_year),
            }),
        )


@admin.register(MediaFile, site=custom_admin_site)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'size', 'description', 'created_at', 'updated_at']
    search_fields = ['file', 'description']
    actions_on_top = False
    actions_on_bottom = False

    def size(self, obj):
        return sizeof_fmt(obj.size_bytes)
