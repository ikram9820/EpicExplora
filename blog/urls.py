from django.urls import path
from .views import *


urlpatterns = [
    path("", post_list,name="posts"),
    path("<int:pk>/",post_detail,name="post_detail")
]