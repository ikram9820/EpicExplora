from django.urls import path
from .views import post_detail,post_list,share_post


urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:id>/',share_post, name='post_share'),
]