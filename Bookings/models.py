from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from hotel.models import *
User = settings.AUTH_USER_MODEL  # points to Users.CustomUser


class UserBooking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    no_of_people = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    no_of_rooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user}"
    
class BookingItem(models.Model):
    booking = models.ForeignKey(
        UserBooking,
        on_delete=models.CASCADE,
        related_name='items'
    )
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.booking} - {self.room}"
    
class Billing(models.Model):
    booking = models.OneToOneField(
        UserBooking,
        on_delete=models.CASCADE,
        related_name='billing'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    stripe_order_id = models.CharField(max_length=255)
    stripe_meta_data = models.JSONField(null=True,blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for Booking #{self.booking.id}"