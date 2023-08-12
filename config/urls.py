from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
 'posts': PostSitemap,
}

urlpatterns = [
    path('', include(('blog.urls', 'blog'), namespace="blog")),
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
