from django import forms
from django.forms import *
from django import template
from django.forms.fields import *
from django.forms.widgets import *
from django.forms import ModelForm
from django.template import loader
from django.contrib.auth.models import User

from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db.models.fields.files import *
from tinymce.widgets import TinyMCE
from form_utils.widgets import *
from form_utils.fields import *
from django.db.models import *

from kenstream.settings import *
from accounts.models import *
from .models import *

# {% load thumbnail %}   
class SimpleForm(forms.ModelForm):
   poster = forms.ImageField(
      widget=ImageWidget()
   )
   review = forms.CharField(
       max_length=350,
       widget=forms.Textarea(attrs={'rows':10,'cols':5}),
   )
   
   def __init__(self, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['poster'].widget.attrs['class'] = 'fileUpoad'
        self.fields['genre'].widget.attrs['class'] = 'fileUpoad'
        self.fields['ratings'].widget.attrs['class'] = 'fileUpoad'
        
   class Meta(object):
       model = Movie
       fields = (
       'title','genre','poster',
       'review','ratings',#'embed_video'
       )
   
   def clean_poster(self):#set min-size
        poster = self.cleaned_data['poster']   
        if 'content-type' in poster:  #require image to be a certain scalable size
            main, sub = poster['content-type'].split('/')  
            if not (main == 'image' and sub in CONTENT_TYPES):  
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.') 
        else:
            return poster     


     
#works with an update view 

class BasicsForm(forms.ModelForm):
    pass 
    """
    def __init__(self, *args, **kwargs):
        super(BasicsForm, self).__init__(*args, **kwargs)
        self.fields['poster'].widget.attrs['class'] = 'fileUpoad'
        self.fields['genre'].widget.attrs['class'] = 'alt=choices'
        
    class Meta(object):
        model = Movie
        fields = (
        'title','genre','video',
        'poster'
        )
    """        
        
class DetailsForm(forms.ModelForm):
    pass 
    """
    review = forms.CharField(
       max_length=350,
       widget=AutoResizeTextarea()
    )
    rating = forms.CharField(
         widget=forms.RadioSelect(
         renderer=StarsRadioFieldRenderer, 
         attrs={'class':'star'}, 
         choices=RATING_CHOICES
         )
     )
    def __init__(self, *args, **kwargs):
        super(DetailsForm, self).__init__(*args, **kwargs)
        #self.fields[''].widget.attrs['class'] = ''
        
    class Meta(object):
        model = Movie
        fields = (
        'cast','review','director',
        'rating'
        )
        
    def clean_review(self):
        review = self.cleaned_data['review']
        if len(self.cleaned_data['review'])> 350:
           raise forms.ValidationError("Review must be less than 350 words")
        else:
            return review
    """           

