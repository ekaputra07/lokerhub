from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from hub.sitemaps import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^lokeradmin/', include(admin.site.urls)),
    url(r'^', include('hub.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
