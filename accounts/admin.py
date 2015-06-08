from django.contrib import admin
from accounts.relatedfield_admin import *
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *
from .forms import *





class CustomUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    
    list_display = ('full_name','phone_number',)
    search_fields = ('phone_number','full_name',)
    list_filter = ('full_name',)
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('is_staff','is_admin')
        return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
    
    
admin.site.register(CustomUser,CustomUserAdmin)


#admin.site.register(CustomUser)

# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
