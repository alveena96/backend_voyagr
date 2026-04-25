from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel
from .serializers import HotelListSerializer, HotelDetailSerializer

from geopy.distance import geodesic

RADIUS_IN_KM =10
def parse_location(location_str):
    """
    Expecting location stored as: "lat,lng"
    Example: "33.6844,73.0479"
    """
    try:
        lat, lng = map(float, location_str.split(','))
        return (lat, lng)
    except:
        return None


class HotelNearbyAPIView(APIView):
    """
    POST:
    {
        "lat": 33.6844,
        "lng": 73.0479
    }
    """

    def post(self, request):
        user_lat = request.data.get("lat")
        user_lng = request.data.get("lng")

        if not user_lat or not user_lng:
            return Response(
                {"error": "lat and lng required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_location = (float(user_lat), float(user_lng))

        hotels = Hotel.objects.all()
        nearby_hotels = []

        for hotel in hotels:
            hotel_coords = parse_location(hotel.location)

            if not hotel_coords:
                continue

            distance = geodesic(user_location, hotel_coords).km

            if distance <= RADIUS_IN_KM:
                nearby_hotels.append(hotel)

        serializer = HotelListSerializer(nearby_hotels, many=True)
        return Response(serializer.data)

class HotelDetailAPIView(APIView):
    """
    GET /hotel/<id>/
    Returns hotel details with ONLY available rooms
    If no rooms available, still returns hotel data with message
    """

    def get(self, request, pk):
        try:
            hotel = Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            return Response(
                {"error": "Hotel not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get available rooms
        available_rooms = hotel.room_types.filter(rooms_available__gt=0)

        # Serialize hotel
        hotel_data = HotelDetailSerializer(hotel).data

        from .serializers import RoomTypeSerializer
        hotel_data['room_types'] = RoomTypeSerializer(available_rooms, many=True).data

        # If no rooms available
        if not available_rooms.exists():
            hotel_data['room_types'] = []
            hotel_data['message'] = "No rooms available for this hotel"

        return Response(hotel_data, status=status.HTTP_200_OK)

    
class RateHotelAPIView(APIView):
    """
    POST:
    {
        "rating": 4
    }
    """

    def post(self, request, pk):
        try:
            hotel = Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            return Response(
                {"error": "Hotel not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        rating = request.data.get("rating")

        if rating is None:
            return Response(
                {"error": "rating is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rating = int(rating)
        except:
            return Response(
                {"error": "rating must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if rating < 0 or rating > 5:
            return Response(
                {"error": "rating must be between 0 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simple overwrite (you can improve later with average system)
        hotel.rating = rating
        hotel.save()

        return Response({
            "message": "Rating updated",
            "rating": hotel.rating
        })