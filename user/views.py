from .models import OTP, User , Deliver , Address
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import random
from .serializer import OTPSerializer, LoginUserSerializer, SignupSerializer , DeliverySerializer
from rest_framework import generics, status
from django.utils import timezone
import datetime
from .authentication import create_access_token

class OTPView(APIView):

    def post(self, request):
        body = json.loads(request.body)
        phone_number = body['phone_number']
        otp = random.randint(10000, 99999)
        OTP.objects.create(
            phone_number=phone_number,
            otp=otp
        )
        return Response(otp)


class CreateOTP(generics.CreateAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = request.data['phone_number']
            otp = random.randint(10000, 99999)
            OTP.objects.filter(phone_number=phone_number).delete()
            OTP.objects.create(
                phone_number=phone_number,
                otp=otp,
                expiration_time=timezone.now() + datetime.timedelta(minutes=5)
            )
            return Response(otp)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data

        return Response({'token': token})


class SignupAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {
                'message': 'User created successfully',
                'token': create_access_token(id=user.id)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDelivery(generics.CreateAPIView):
    queryset = Deliver.objects.all()
    serializer_class = DeliverySerializer

    def perform_create(self, serializer):
        print(self.request.data)
        origin_address = Address.objects.create(**self.request.data['origin'])
        destination_address = Address.objects.create(**self.request.data['destination'])
        serializer.save(origin=origin_address,destination=destination_address)