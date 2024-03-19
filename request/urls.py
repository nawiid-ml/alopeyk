from django.urls import  path , include
from .views import RouterView , RouterListview

urlpatterns = [
    path('router',RouterView.as_view()),
    path('router/list',RouterListview.as_view(),)

]
