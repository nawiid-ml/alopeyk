from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Router
from .serializer import RouterSerializer
from googlemaps import distance_matrix
import neshan

NESHAN_API_KEY = "web.47a257d4840d4ccba5ac2d0b4f8370b7"

class RouterView(generics.CreateAPIView):
    """
        API endpoint for creating a new Router object with route information.

    This view class inherits from `generics.CreateAPIView` but restricts HTTP methods to POST only (`http_method_names = ['post']`).
    - It expects request data containing origin and destination latitude/longitude coordinates.
    - Upon receiving a POST request:
        - Extracts origin and destination coordinates from the request data.
        - Creates a `NeshanAPI` instance using your API key.
        - Calls the `NeshanAPI.get_route_info` method to retrieve route information 
          based on the provided coordinates.
        - Returns the retrieved route information (presumably a dictionary or JSON) in the response.
    """
    queryset = Router.objects.all()
    serializer_class = RouterSerializer
    http_method_names = ['post']

    
    def post(self, request, *args, **kwargs):
        # دریافت طول و عرض جغرافیایی از درخواست
        origin_latitude = request.data.get("origin_latitude")
        origin_longitude = request.data.get("origin_longitude")
        destination_latitude = request.data.get("destination_latitude")
        destination_longitude = request.data.get("destination_longitude")

        # ایجاد یک نمونه از کلاس NeshanAPI
        neshan_api = neshan(NESHAN_API_KEY)

        # دریافت اطلاعات مسیر
        route_info = neshan_api.get_route_info(
            origin_latitude=origin_latitude,
            origin_longitude=origin_longitude,
            destination_latitude=destination_latitude,
            destination_longitude=destination_longitude,
        )
        # ارسال پاسخ به کاربر
        return Response(route_info, status=status.HTTP_200_OK)


class RouterListview(generics.ListAPIView):
    """
    API endpoint for retrieving a list of all existing Router objects.

    This view class inherits from `generics.ListAPIView` and restricts HTTP methods to GET only (`http_method_names = ['get']`).
    - It returns a list of all `Router` objects serialized using the `RouterSerializer`.
    """
    queryset = Router.objects.all()
    serializer_class = RouterSerializer
    http_method_names = ['get']
        