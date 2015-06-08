from __future__ import(
absolute_import, unicode_literals
) 


from django.db import models
from django.db.models import *
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import *
from django.contrib.auth.signals import user_logged_in


from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from kenstream.settings import *


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        now = timezone.now()
        if not phone_number:
            raise ValueError('The given phone number must be set')
        #email = UserManager.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          is_staff=False,is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, phone_number, password, **extra_fields):
        u = self.create_user(phone_number, password, **extra_fields)
        u.is_admin = True
        u.save(using=self._db)
        return u

# Users are going to eventually pay for the streaming service
# so we need a custom user model eventually
class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(
       max_length=50,db_index=True,
       verbose_name='First & Last Name'
    )
    phone_number = models.CharField(
       max_length=15,unique=True,
       verbose_name='Phone Number'
    )
    photo = models.ImageField(
       upload_to='/images/profiles',
       verbose_name ='Profile Photo',
       null=True,blank=True
    )
    gender = models.CharField(
       max_length=1,choices=settings.GENDER,
       verbose_name='Select Gender',
       default=1
    )
    email = models.EmailField(
       max_length=100,null=True,
       verbose_name='E-mail Address',
       blank=True
    )
    description = HTMLField(
       max_length=350,null=True,blank=True,
       verbose_name='About Yourself'  
    )
    is_staff = models.BooleanField(
       default=False
    )
    #is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
       auto_now_add=True
    )
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name',]
    
    objects = CustomUserManager()
    
    class Meta(object):
        db_table='CustomUser'
        ordering = ['date_joined']
        verbose_name_plural='CustomUsers'
        
    def __unicode__(self):
        return self.full_name
        
    
    
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.full_name)
           
    def get_full_name(self):
        #the user is identified by their id_number
        return self.full_name
        
    def get_short_name(self):
        return self.full_name
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
   
    def save(self,*args,**kwargs):
        super(CustomUser,self).save(*args,**kwargs)
        

