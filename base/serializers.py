from django.db.models import fields
from rest_framework import serializers
from base.models import Client, Medicament, Pharmacien, Pharmacie, Commande


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model= Client
        fields= ('id','first_name','last_name','date_naissance','phone')


class MedicamentSerializers(serializers.ModelSerializer):
    class Meta:
        model= Medicament
        fields= ('__all__')


class PharmacienSerializers(serializers.ModelSerializer):
    class Meta:
        model= Pharmacien
        fields= ('__all__')


class PharmacieSerializers(serializers.ModelSerializer):
    class Meta:
        model= Pharmacie
        fields= ('__all__')


class CommandeSerializers(serializers.ModelSerializer):
    class Meta:
        model= Commande
        fields= ('__all__')