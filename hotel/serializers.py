from rest_framework import serializers
from .models import *



class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            'id',
            'room_type',
            'total_rooms',
            'rooms_available',
            'people_per_room',
            'price'
        ]


class HotelListSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'rating',
            'short_info',
            'price_range',
            'refund_percentage',
            'location',
            'pictures'
        ]


class HotelDetailSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'rating',
            'short_info',
            'price_range',
            'refund_percentage',
            'location',
            'pictures',
            'room_types'
        ]


