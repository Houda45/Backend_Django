from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

class otp(models.Model):
    phone = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    
    def _str_(self):
        return   self.key + ' :  est le code de user : '+self.phone
    

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, nni, phone, last_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(nni, phone, last_name, first_name, password, **other_fields)

    def create_user(self, nni, phone,  last_name, first_name, password, **other_fields):

        # if not email:
        #     raise ValueError(_('You must provide an email address'))

        # email = self.normalize_email(email)
        user = self.model(nni=nni,phone=phone,  last_name=last_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class Client(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    start_date = models.DateTimeField(default=timezone.now)
    phone= models.CharField(unique=True, max_length=30)
    number_attempt= models.IntegerField(default=0)
    number_attempt_otp = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    date_naissance = models.DateField()
    
    # username= None

    objects = CustomAccountManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'nni']

    def __str__(self):
        return self.last_name

