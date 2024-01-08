from django.urls import path
from . import views
from .views import ClientViews, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('sms', views.SendSms),
    path('client', ClientViews.as_view()),
    path('passwordsetup',views.passwordsetup),
    path('smsback', views.otp_verfication),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
