from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
 'posts': PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace="blog")),
    path('account/', include('account.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
]
