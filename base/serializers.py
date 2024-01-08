from django.db.models import fields
from rest_framework import serializers
from base.models import Client


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model= Client
        fields= ('first_name','last_name','date_naissance','phone')

