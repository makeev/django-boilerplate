from django.urls import path

from .views import PostList, PostDetail

app_name = 'news'


urlpatterns = [
    # новый способ записи url начиная с django>2.0
    path('news/', view=PostList.as_view(), name='post_list'),
    path('news/<slug:slug>/', view=PostDetail.as_view(), name='post_detail'),
]
