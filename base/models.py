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


class Medicament(models.Model):
    nom = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    types = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='img', blank=True)

    def __str__(self):
        return self.nom
    

class Pharmacien(AbstractBaseUser):
     nom = models.CharField(max_length=255)
     telephone = models.CharField(max_length=20)
     adresse = models.TextField()
     
     objects = CustomAccountManager()
     USERNAME_FIELD = 'telephone'
     REQUIRED_FIELDS = ['nom', 'telephone', 'adresse']

     def __str__(self):
        return self.nom
     

class Pharmacie(models.Model):
    pharmacien = models.ForeignKey(Pharmacien, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    def __str__(self):
        return self.nom
    

class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.medicament} - {self.client} - {self.date}"
