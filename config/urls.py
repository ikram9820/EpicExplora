from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace="blog")),
    path("__debug__/", include("debug_toolbar.urls")),
]
