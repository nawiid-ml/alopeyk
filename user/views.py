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
    """
    API endpoint for generating a new OTP and sending it (implementation not provided).

    This view class handles POST requests. 
    - It retrieves the phone number from the request body.
    - Generates a random 5-digit OTP code.
    - Creates a new OTP object in the database with the phone number and code.
    - Returns the generated OTP in the response (likely for display or sending to the user).

    **Security Considerations:**
    - This approach directly returns the OTP in the response, which might not be ideal for security reasons. 
    - Consider implementing a mechanism to send the OTP securely (e.g., SMS, email).
    """    

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
    """
    API endpoint for creating a new OTP object with phone number and expiration time.

    This view class inherits from `generics.CreateAPIView` for simplified object creation.
    - It validates data using `OTPSerializer`.
    - Retrieves the phone number from the request data.
    - Generates a random 5-digit OTP code.
    - Deletes any existing OTP for the provided phone number (prevents duplicate OTPs).
    - Creates a new OTP object with the phone number, code, and expiration time (default 5 minutes).
    - Returns a successful response with the generated OTP code upon successful creation.    
    """
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
    """API endpoint for user login using phone number and OTP verification.

    This view class handles POST requests.
    - It validates login credentials with `LoginUserSerializer`.
    - The serializer performs OTP verification and authentication logic.
    - Upon successful login, a token is generated and returned in the response.
    """
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data

        return Response({'token': token})


class SignupAPI(generics.CreateAPIView):
    """
    API endpoint for user signup using `SignupSerializer`.

    This view class inherits from `generics.CreateAPIView` for simplified object creation.
    - It validates signup data using `SignupSerializer`.
    - Upon successful validation, it creates a new User object.
    - Generates an access token for the newly created user and returns it in a successful response.
    """   
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
    """
    API endpoint for creating a new delivery request.

    This view class inherits from `generics.CreateAPIView` for simplified object creation.
    - It expects a serialized representation of a delivery request in the request body.
    - In `perform_create()`, it performs the following steps:
        1. Prints the entire request data for debugging purposes (can be removed in production).
        2. Extracts the nested 'origin' and 'destination' dictionaries from the request data.
        3. Creates separate `Address` objects for the origin and destination using the extracted dictionaries.
            - The `**` operator unpacks the dictionary keys and values as keyword arguments for `Address.objects.create()`.
        4. Calls the `save()` method on the `DeliverySerializer` instance, passing the created `origin_address` and `destination_address` objects.
            - This saves a new `Deliver` object with the provided origin and destination addresses.
    """    
    queryset = Deliver.objects.all()
    serializer_class = DeliverySerializer

    def perform_create(self, serializer):
        origin_data = self.request.data['origin']
        destination_data = self.request.data['destination']

        origin_address = Address.objects.create(**origin_data)
        destination_address = Address.objects.create(**destination_data)

        serializer.save(origin=origin_address, destination=destination_address)