from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('slug', 'user', 'title', 'annotation', 'content',
                  'get_absolute_url',)
