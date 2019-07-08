from boolean_switch.admin import AdminBooleanMixin

# from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Post
from project.admin import admin_register


@admin_register(Post)
class PostAdmin(AdminBooleanMixin, AdminImageMixin, TranslationAdmin):
    list_display = ('title', 'is_published', 'published_at',)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'published_at'
    list_filter = ('is_published', 'user',)
    search_fields = ('title', 'slug', '=pk',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
