from .views import OTPView, CreateOTP, LoginAPI, SignupAPI , RequestDelivery
from django.urls import path

urlpatterns = [
    path('otp-code', OTPView.as_view()),
    path('create-otp', CreateOTP.as_view()),
    path('login', LoginAPI.as_view()),
    path('signup', SignupAPI.as_view()),
    path('request-deliver',RequestDelivery.as_view())
]
