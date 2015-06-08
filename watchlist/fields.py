from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

__all__ = ('EmbedVideoField', 'EmbedVideoFormField')


class EmbedVideoField(models.URLField):
    pass 
    
    
class EmbedVideoFormField(forms.URLField):
    pass 
