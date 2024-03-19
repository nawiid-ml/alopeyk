from rest_framework.serializers import Serializer
from .models import Router


class RouterSerializer(Serializer):
    class Meta:
        model = Router
        fields = '__all__'