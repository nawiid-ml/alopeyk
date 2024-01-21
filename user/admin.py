from django.contrib.admin import register, ModelAdmin
from .models import OTP , User , Deliver , Address


@register(OTP)
class OTPAdmin(ModelAdmin):
    readonly_fields = ('expiration_time',)
    ...

@register(User)
class UserAdmin(ModelAdmin):
    ...

@register(Deliver)
class DeliverAdmin(ModelAdmin):
    ...

@register(Address)
class AddressAdmin(ModelAdmin):
    ...    