from django.urls import path
from .views import (
    HotelNearbyAPIView,
    HotelDetailAPIView,
    RateHotelAPIView
)

urlpatterns = [
    path('hotels-nearby/', HotelNearbyAPIView.as_view(), name='nearby-hotels'),
    path('hotels/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('hotels/<int:pk>/rate/', RateHotelAPIView.as_view(), name='rate-hotel'),
]