from .models import OTP, User, Deliver, Address
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .authentication import create_access_token
from django.utils import timezone


class OTPSerializer(ModelSerializer):
    """
    Handles serialization of OTP model instances, specifically for the 'phone_number' field.
    Likely used for retrieving the phone number associated with a given OTP.
    """
    class Meta:
        model = OTP
        fields = ('phone_number',)


class LoginUserSerializer(Serializer):
    """
    Handle user login process, involving phone number and OTP verification.
    Upon successful validation, returns an access token for the authenticated user.
    """    
    phone_number = serializers.CharField()
    code = serializers.CharField(
        style={'phone_number': 'code'}, trim_whitespace=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        user_code = data.get('code')

        if phone_number and user_code:
            try:
                otpObject = OTP.objects.get(phone_number=phone_number)
                otpCode = otpObject.otp
                hasExpire = otpObject.expiration_time < timezone.now()
                print(f"now: {timezone.now()} exp:{otpObject.expiration_time}")
                if otpCode == user_code and not hasExpire:
                    # otpObject.delete()
                    try:
                        user = User.objects.get(phone_number=phone_number)
                        print(user.id)
                        token = create_access_token(id=user.id)
                        return token

                    except User.DoesNotExist:
                        raise serializers.ValidationError('User not found')

                    except Exception as e:
                        raise e
                else:
                    raise serializers.ValidationError('Code Verify Failed')
            except OTP.DoesNotExist:
                raise serializers.ValidationError('Code Verify Failed')
        else:
            raise serializers.ValidationError('Please enter required fields')


class SignupSerializer(ModelSerializer):
    """
    Handles serialization of User model instances, likely for user signup functionality.
    """    
    class Meta:
        model = User
        fields = '__all__'


class AddressSerializer(ModelSerializer):
    """
    Handles serialization of Address model instances.
    """    
    class Meta:
        model = Address
        fields = '__all__'


class DeliverySerializer(ModelSerializer):
    """
    Handles serialization of Deliver model instances, including nested serialization of origin and destination addresses.
    """    
    origin = AddressSerializer()
    destination = AddressSerializer()
    
    class Meta:
        model = Deliver
        fields = '__all__'
