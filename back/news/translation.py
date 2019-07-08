from modeltranslation.translator import TranslationOptions, translator

from .models import Post


class PostTranslation(TranslationOptions):
    fields = ('title', 'annotation', 'content',)


translator.register(Post, PostTranslation)
