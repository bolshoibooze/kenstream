from django.contrib import admin
#from embed_video.admin import AdminVideoMixin
from .models import *


class GenreAdmin(admin.ModelAdmin):
    fieldsets = ('Genre',{
       'fields': ('name',)
    }),
    list_display = ('name',)
    list_filter = ( 'name',)
    search_fields = ('name',)
    exclude = ('user',)
       
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
    
admin.site.register(Genre,GenreAdmin)


class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Title & Genre',{
       'fields':('title','genre')
    }),
    ('Movie Poster',{
       'fields':('poster',)
    }),
    ('Review',{
       'fields':('ratings','review',)
    }),
   
    )
    list_display = ('title','genre',)
    search_fields = ('title','genre',)
    list_filter = ('genre',)
    exclude = ('user',)
       
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
    
admin.site.register(Movie,MovieAdmin)
    
    




