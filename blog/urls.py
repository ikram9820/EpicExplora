from django.urls import path
from .views import delete_confirm, delete_post, post_comment, post_detail,post_list, post_search,share_post, edit_post,add_post
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('add/', add_post, name='add_post'),
    path('<int:pk>/edit/', edit_post, name='edit_post'),
    path('<int:pk>/delete/confirm/', delete_confirm, name='delete_confirm'),
    path('<int:pk>/delete/', delete_post, name='delete_post'),
    path('<int:id>/share/',share_post, name='post_share'),
    path('<int:id>/comment/',post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),


]