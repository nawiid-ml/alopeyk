from .models import OTP, User, Deliver, Address
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .authentication import create_access_token
from django.utils import timezone


class OTPSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = ('phone_number',)


class LoginUserSerializer(Serializer):
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
    class Meta:
        model = User
        fields = '__all__'


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class DeliverySerializer(ModelSerializer):
    origin = AddressSerializer()
    destination = AddressSerializer()
    
    class Meta:
        model = Deliver
        fields = '__all__'
