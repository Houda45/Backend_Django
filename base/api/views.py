import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
from twilio.rest import Client as cli
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import  permissions, generics, status
from django.contrib.auth.hashers import make_password

from base.models import otp, Client
from base.serializers import ClientSerializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)





@api_view(['POST'])
def SendSms(request):
    account_sid = "ACba695597bfe49e5464e90216631e4eb0"
    auth_token = "5a436e44cab04934bb74fd79b70f8ce6"
    data = request.data
    phone = data['phone']
    try:
        user=Client.objects.get(phone=phone)
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':'Numéro déja existe'})
    except :
        verified_number = "+222"+phone
        key = str(random.randint(100000, 999999))
        try:
            user = otp.objects.get(phone=phone)
            user.delete()
        except:
            pass
        client = cli(account_sid, auth_token)
        try:
            message = client.messages.create(
                body=f'votre code est {key}',
                from_='+16184946224',
                to=verified_number
                )
            otp.objects.create(phone=phone,key=key)
        except:
            pass
        # print(message.sid)
        print(key)
        return Response({'status':status.HTTP_200_OK, 'message':'Otp envoyé avec succès'})
    
@api_view(['POST'])
def otp_verfication(request):
    data = request.data
    phone = data['phone']
    key = data['key']
    try:
        if key == '':
            return Response({'message':'Entrez le code!', 'status':status.HTTP_400_BAD_REQUEST})
        try:
            user = otp.objects.get(phone=phone, key=key)
            if user:
                user.delete()
                return Response({'message':'code confirmer ', 'status': status.HTTP_200_OK})
            return Response({'message':'code incorrect !', 'status': status.HTTP_400_BAD_REQUEST})
        except:
            return Response({'message':'code incorrect!', 'status': status.HTTP_400_BAD_REQUEST})

    except:
        return Response({'message':'code invalid!', 'status':status.HTTP_400_BAD_REQUEST})
    


class ClientViews(APIView):
    permission_classes = (permissions.AllowAny,)
    #permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Client.objects.all()
        serializer = ClientSerializers(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer= ClientSerializers(data= request.data)
        if serializer.is_valid():
            # print(serializer.validated_data.get('first_name'))
            phone= serializer.validated_data.get('phone')
           

            if len((phone)) != 8:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'phone': 'Le telephone doit contenir 8 chiffres'})
            serializer.save(is_staff=1)
            return Response({ 'message': serializer.data , 'status':status.HTTP_200_OK})
        # data= serializer.errors
        # print(data['nni'][0])
        return Response({'message': 'Données incomplètes', 'status': status.HTTP_400_BAD_REQUEST})


@api_view(['POST'])
def passwordsetup(request):
    data = request.data
    phone = data['phone']
    password=make_password(data['password'])
    try:
        user=Client.objects.get(phone=phone)
    except:
        return Response({'message':'Ultilisateur ne existe pas','status':status.HTTP_400_BAD_REQUEST})
    user.password=password
    user.save()
    return Response({'message':'Success','status':status.HTTP_200_OK})



  