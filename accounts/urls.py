from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth.decorators import login_required
from .models import *
from .views import *


urlpatterns = patterns('accounts.views',

    url(r'^login/$',LoginView.as_view(),
        name = 'login'),
        
    url(r'^logout/$','logout_view',name='logout'),
    
    #url(r'^lockout/$',AccountLockView.as_view(),name = 'lockout'),
        
      
    url(r'^signup$',RegistrationView.as_view(),
        name = 'signup'),
    
 
        
    url(r'^redirect/$',RegSuccessView.as_view(),
        name = 'redirect'),
        
    
    #url(r'^password/(?P<pk>\d+)/$',ChangePasswordFormView.as_view(),name='password'),
        
   

)
