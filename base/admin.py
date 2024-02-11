from django.contrib import admin

from base.models import otp, Client, Medicament, Pharmacien, Pharmacie, Commande

# Register your models here.

admin.site.register(otp)

admin.site.register(Client)

admin.site.register(Medicament)

admin.site.register(Pharmacien)

admin.site.register(Pharmacie)

admin.site.register(Commande)
