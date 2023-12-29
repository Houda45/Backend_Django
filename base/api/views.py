import random
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
from twilio.rest import Client as cli
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import  permissions, generics, status

from base.models import otp

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
    data = request.data
    phone = data['phone']
    account_sid = "ACba695597bfe49e5464e90216631e4eb0"
    auth_token = "5a436e44cab04934bb74fd79b70f8ce6"
    #verify_sid = os.environ["YOUR_VERIFY_SID"]
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
    return Response(key)
    
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
  