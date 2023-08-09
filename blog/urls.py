from django.urls import path
from .views import post_comment, post_detail,post_list,share_post


urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:id>/share/',share_post, name='post_share'),
    path('<int:id>/comment/',post_comment, name='post_comment')
]