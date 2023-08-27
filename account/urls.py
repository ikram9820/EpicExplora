from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/<str:author>', views.dashboard, name='user_dashboard'),
    path('tag/<slug:tag_slug>/',views.dashboard, name='dashboard_with_tags'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]

