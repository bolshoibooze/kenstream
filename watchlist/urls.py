from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .views import *


urlpatterns = patterns('watchlist.views',


    #url(r'^post/$',login_required(PostReviewWizard.as_view(BasicsForm,DetailsForm)),name='post'),
    
    #url(r'^create/$',login_required(PostReview.as_view()),name='create'),
    url(r'^create/$',PostReview.as_view(),name='create'),

    #url(r'^edit/(?P<slug>[a-zA-Z0-9-]+)$',login_required(EditReview.as_view()),name = 'edit'),
     
    url(r'^edit/(?P<slug>[a-zA-Z0-9-]+)$',EditReview.as_view(),name = 'edit'), 
      
    url(r'^watchlist/$',WatchListView.as_view(),
        name='watchlist'),
        
    url(r'^movie/(?P<slug>[a-zA-Z0-9-]+)/$',WatchDetailView.as_view(),
        name='movie'),
        
    url(r'^delete/(?P<slug>[a-zA-Z0-9-]+)/$',login_required(DeleteReview.as_view()),
        name='delete'),
    
    url(r'^documentaries/$',DocumentariesListView.as_view(),
        name='documentaries'),
        
    url(r'^series/$',SeriesListView.as_view(),
        name='series'),
        
    url(r'^classics/$',ClassicsListView.as_view(),
        name='classics'),
    
    url(r'^tv/$',TvShowsListView.as_view(),
        name='tv'),
        
    #url(r'^genre/$',GenreListView.as_view(),name='genre'),
    
    #url(r'^/$',login_required(),name=''),
            
    #url(r'^/$',login_required(),name),
        
    
        
        
        
)
