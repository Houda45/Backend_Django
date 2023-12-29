from django.db import models

# Create your models here.

class otp(models.Model):
    phone = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    
    def _str_(self):
        return   self.key + ' :  est le code de user : '+self.phone