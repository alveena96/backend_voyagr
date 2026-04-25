from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateBookingAPIView.as_view(), name='create-booking'),
    path('my/', UserBookingsAPIView.as_view(), name='user-bookings'),
    path('cancle/<int:pk>/', CancelBookingAPIView.as_view(), name='cancel-booking'),
]