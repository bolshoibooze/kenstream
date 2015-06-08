from django import forms
from django.forms import *
from django import template
from django.forms.fields import *
from django.forms.widgets import *
from django.forms import ModelForm
from django.template import loader
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import *
from django.contrib.auth.forms import *
from django.core import validators
from form_utils.widgets import *
from form_utils.fields import *
from django.db.models import *


from kenstream.settings import *
from accounts.models import *
from .models import *

class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.verbose_name
                })

attrs_dict = {'class': 'required'}

# see :http://stackoverflow.com/questions/4101258/how-do-i-add-a-placeholder-on-a-charfield-in-django

#widget=forms.TextInput(attrs={'placeholder': ''}) 

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("Phone Number already exists.")
    }
    password1 = forms.CharField(
       max_length=50,
       widget=forms.PasswordInput()
    )
    phone_number = forms.CharField(
       max_length=15
    )
    photo = forms.ImageField(
      widget=ImageWidget()
    )
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'fileUpoad'

       
        

    class Meta:
        model = get_user_model()
        fields = (
        "full_name","photo",
        "phone_number",
        )
        
      
           
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        try:
            get_user_model().objects.get(phone_number=phone_number)
        except get_user_model().DoesNotExist:
            return id_number
        raise forms.ValidationError("A user with that Phone Number already exists.")
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) == 0:
            raise forms.ValidationError("Please choose a password.")
        return password1
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        
        if len(full_name) > 50:
            raise ValidationError(_('Your name should not exceed 50 characters'))
        return full_name
        
    
    
          
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


                
           
        
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
      
                           

        
#widget=forms.TextInput(attrs={'placeholder': ''})   
               
class MyAuthForm(forms.Form):
    username = forms.CharField(
    max_length=254
    )
    password = forms.CharField(
    widget=forms.PasswordInput()
    ) 
    
    error_messages = {
        'invalid_login': _("Please enter a correct Phone Number and Password. "
                           ),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }
   
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(MyAuthForm, self).__init__(*args, **kwargs)
    
            
   

        # Set the label for the "username" field.
        UserModel = get_user_model()
        

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    #throws errors:to be deleted
    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


               

    
class MyPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two PINs  didn't match."),
    }
    old_password = forms.CharField(
       label=_("Current Password"),
       widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
       label=_("New Password"),
       widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
       label=_("Confirm Password"),
       widget=forms.PasswordInput()
    )
    
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
   
    def clean_old_password(self):
        UserModel = get_user_model()
        old_password = self.cleaned_data["old_password"]
        self.users_cache = UserModel._default_manager.filter(
        password__iexact=password
        )
        if not len(self.users_cache):
            raise forms.ValidationError(
                self.error_messages['pin_incorrect']
                )
    """  
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
                raise forms.ValidationError(
                self.error_messages['pin_incorrect'])
        #if self.old_password:
            #self.user_cache = authenticate(old_password)
            #if self.user_cache is None:
                raise forms.ValidationError(
                self.error_messages['pin_incorrect'])
        return old_password
    """ 
        
    def clean_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
        
            

