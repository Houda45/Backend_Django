from django.urls import path
from . import views
from .views import ClientDetailViews, ClientViews, CommandeDetailViews, MedicamentDetailViews, MyTokenObtainPairView, MedicamentViews, PharmacieDetailViews, PharmacienDetailViews, PharmacienViews, PharmacieViews, CommandeViews
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('sms', views.SendSms),

    path('client', ClientViews.as_view()),
    path('medicament', MedicamentViews.as_view()),
    path('pharmacien', PharmacienViews.as_view()),
    path('pharmacie', PharmacieViews.as_view()),
    path('commande', CommandeViews.as_view()),
    path('commande/<int:pk>/', CommandeDetailViews.as_view()),
    path('pharmacie/<int:pk>/', PharmacieDetailViews.as_view(), name='pharmacie-detail'),
    path('pharmacien/<int:pk>/', PharmacienDetailViews.as_view(), name='pharmacien-detail'),
    path('medicament/<int:pk>/', MedicamentDetailViews.as_view(), name='medicament-detail'),
    path('client/<int:pk>/', ClientDetailViews.as_view(), name='client-detail'),

    path('passwordsetup',views.passwordsetup),
    path('smsback', views.otp_verfication),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
