from django.urls import path
from .views import *

urlpatterns = [
    path('city', cities),
    path('street', streets_by_city_id),
    path('shop', create_shop)
]
