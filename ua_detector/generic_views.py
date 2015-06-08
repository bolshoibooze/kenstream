
from django.http import *
from django.http import *
from django.shortcuts import *
from django.views import generic
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView
from django.contrib.formtools.wizard.views import *
from django.core.files.storage import FileSystemStorage
from django.views.generic.list import ListView
from django.views.generic.edit import (
CreateView, UpdateView, DeleteView
) 

from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from ua_detector import utilities


__all__ = (
     'MobileDetailView','MobileFormView','MobileTemplateView',
     'MobileRedirectView','MobileListView','MobileToggleListView'
   
)

class MobileMixin(object):
    """
    MobileMixin is a supplement to django's generic views.

    The mobile mixin uses the user agent to match a regular expression
    that is know to indicate a mobile device.

    If the device is mobile and the user doesn't have a 'no_mobile'
    cookie set, the Mixin will try to render the mobile template if
    it exists, falling back to the regular template if not.

    """
    template_name = None
    mobile_template_name = None
    #basic_mobile_template = None
    
    

    def use_mobile(self):
        return utilities.use_mobile(self.request)

    def set_mobile_cookie(self, response):
        response.set_cookie('no_mobile', True)

    def delete_mobile_cookie(self, response):
        response.delete_cookie('no_mobile')

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.use_mobile():
            return self.get_mobile_template_name()
        else:
            return self.get_default_template_name()

    def get_default_template_name(self):
        if self.template_name is None:
            return []
        return [self.template_name]

    def get_mobile_template_name(self):
        if self.mobile_template_name is None:
            return self.get_default_template_name()
        return [self.mobile_template_name]

    def _get_next(request):
        next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
        if not next or next == request.path:
            raise Http404 
        return next

# The views below just piggyback on django's generic views
# adding the mobile mixin...

#Get your feather duster & work on AJAX/Json response

class MobileToggleListView(MobileMixin,ListView):
    """
    Handles requests to turn on/off a toggle.
    """
    http_method_names = ('put', 'delete')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(MobileToggleListView, self).dispatch(request, *args, **kwargs)
        
    

class MobileListView(MobileMixin,ListView):
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MobileListView, self).dispatch(*args, **kwargs)

class MobileTemplateView(MobileMixin, generic.TemplateView):
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MobileTemplateView, self).dispatch(*args, **kwargs)
    


class MobileDetailView(MobileMixin, generic.DetailView):
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MobileDetailView, self).dispatch(*args, **kwargs)

class MobileFormView(MobileMixin, generic.FormView):
    @method_decorator(csrf_protect)
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MobileFormView, self).dispatch(*args, **kwargs)
    
    

class MobileCreateView(MobileMixin, generic.CreateView):
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MobileCreateView, self).dispatch(*args, **kwargs)
        



    
        
class MobileRedirectView(MobileMixin, generic.RedirectView):
    permanent = False
    


