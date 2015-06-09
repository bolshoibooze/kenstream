from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from yawdadmin import admin_site
admin_site._registry.update(admin.site._registry)
from accounts.views import IndexRedirectView


urlpatterns = patterns('',
    url(r'^$',IndexRedirectView.as_view()),
    
    url(r'^accounts/', include('accounts.urls')),
    url(r'^watchlist/',include('watchlist.urls')),
    url(r'^ua_detector/',include('ua_detector.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^likes/', include('likes.urls')),
    #url(r'^/',include('.urls')),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^post/comments/', include('fluent_comments.urls')),
    #url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^darknet/', include(admin.site.urls)),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
urlpatterns += staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media_url"),
) + urlpatterns
"""

