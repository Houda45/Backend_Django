import random
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
import os
from twilio.rest import Client as cli
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import  permissions, generics, status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import otp, Client, Medicament, Pharmacien, Pharmacie, Commande
from base.serializers import ClientSerializers, MedicamentSerializers, PharmacienSerializers, PharmacieSerializers, CommandeSerializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  # Assurez-vous d'ajuster le chemin d'accès au numéro de téléphone en fonction de votre modèle d'utilisateur

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data
        """user = serializer.validated_data['user']"""
        response.data.update({
            'message': "login succès",
            'staus':status.HTTP_200_OK
        })
        return response

class Mytoken(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return refresh

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


class ClientDetailViews(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializers(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MedicamentViews(APIView):
    permission_classes = (permissions.AllowAny,)
    #permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Medicament.objects.all()
        serializer = MedicamentSerializers(query, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = MedicamentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicamentDetailViews(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get_object(self, pk):
        try:
            return Medicament.objects.get(pk=pk)
        except Medicament.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        medicament = self.get_object(pk)
        serializer = MedicamentSerializers(medicament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        medicament = self.get_object(pk)
        medicament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PharmacienViews(APIView):
    permission_classes = (permissions.AllowAny,)
    #permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Pharmacien.objects.all()
        serializer = PharmacienSerializers(query, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PharmacienSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmacienDetailViews(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get_object(self, pk):
        try:
            return Pharmacien.objects.get(pk=pk)
        except Pharmacien.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        pharmacien = self.get_object(pk)
        serializer = PharmacienSerializers(pharmacien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pharmacien = self.get_object(pk)
        pharmacien.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PharmacieViews(APIView):
    permission_classes = (permissions.AllowAny,)
    #permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Pharmacie.objects.all()
        serializer = PharmacieSerializers(query, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PharmacieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmacieDetailViews(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get_object(self, pk):
        try:
            return Pharmacie.objects.get(pk=pk)
        except Pharmacie.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        pharmacie = self.get_object(pk)
        serializer = PharmacieSerializers(pharmacie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pharmacie = self.get_object(pk)
        pharmacie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    

class CommandeViews(APIView):
    permission_classes = (permissions.AllowAny,)
    #permission_classes = [IsAuthenticated, ]
    def get(self, request):
        query = Commande.objects.all()
        serializer = CommandeSerializers(query, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CommandeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommandeDetailViews(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        commande = self.get_object(pk)
        serializer = CommandeSerializers(commande, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        commande = self.get_object(pk)
        commande.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)