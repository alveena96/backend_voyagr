from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    short_info = models.TextField()
    price_range = models.CharField(max_length=100)
    refund_percentage = models.FloatField(default=100)
    location = models.TextField() 

    def __str__(self):
        return self.name


def hotel_image_path(instance, filename):
    return f"hotels/{instance.hotel.id}/{filename}"


class Picture(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_image_path)

    def __str__(self):
        return f"Image for {self.hotel.name}"

    def delete(self, *args, **kwargs):
        # delete file from storage
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)



class RoomType(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='room_types'
    )
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE_CHOICES
    )
    total_rooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    rooms_available = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    people_per_room = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"