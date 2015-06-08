
from django.conf.urls import patterns, include, url

from ua_detector import views

urlpatterns = patterns('',
    url(r'full-site/$', views.FullSiteView.as_view(), name="full_site"),
)
