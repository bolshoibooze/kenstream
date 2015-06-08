import datetime
from decimal import *
from django.db import models
from django.db.models import *
from datetime import timedelta
from django.conf import settings
from django.db.models.query import QuerySet
from django.contrib.auth.models import *
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils.encoding import smart_unicode
from django.utils.text import slugify


from tinymce.models import HTMLField
from .fields import EmbedVideoField

#stying the ratings:
# source: http://www.fyneworks.com/jquery/star-rating/#tab-Overview
# tutorial: http://www.azavea.com/blogs/labs/2011/04/jquery-star-rating-with-django-ratings/

class RatingField(IntegerField):
    pass

class Genre(models.Model):
    name = models.CharField(
       max_length=50,verbose_name='Name'
    )
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='admin'
    )
    class Meta(object):
        db_table = 'Genre'
        verbose_name_plural = 'Genres'
        
    def __unicode__(self):
        return self.name
        
        
    def save(self,*args,**kwargs):
        super(Genre,self).save(*args,**kwargs)
        
class Movie(models.Model):
    title = models.CharField(
       max_length=50,db_index=True,
       verbose_name = 'Title'
    )
    genre = models.ForeignKey(
       Genre,related_name='+',
       verbose_name='Select Genre'
    )
    poster = models.ImageField(
       upload_to='uploads/%Y/%m/%d',
       verbose_name='Poster',
       null=True,blank=True
    )
    video = EmbedVideoField(
       verbose_name='Embed Video',
       null=True,blank=True
    )
    original_video = models.FileField(
       upload_to='.',
       verbose_name='Upload Video',
       null=True,blank=True
    )
    cast = HTMLField(
       max_length=140,verbose_name='Cast',
       null=True,blank=True
    )
    director = HTMLField(
       max_length=140,verbose_name='Director',
       null=True,blank=True 
    )
    review = HTMLField(
       max_length=350,verbose_name='Review',
       help_text='html content',
    )
    views = models.IntegerField(default=0)
    enable_comments = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    editors_pick = models.BooleanField(default=False)
    edited_on = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100)
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    class Meta(object):
        db_table = 'Movie'
        verbose_name_plural = 'Movies'
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        """
        return ('video_detail', (), { 
            'year': self.timestamp.strftime("%Y"),
            'month': self.timestamp.strftime("%b"),
            'day': self.timestamp.strftime("%d"), 
            'slug': self.slug 
        })  
        """
        pass 
        
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Movie,self).save(*args,**kwargs)
        

from ratings.handlers import ratings
ratings.register(Movie)
