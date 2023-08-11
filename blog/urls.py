from django.urls import path
from .views import post_comment, post_detail,post_list, post_search,share_post
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:id>/share/',share_post, name='post_share'),
    path('<int:id>/comment/',post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),


]