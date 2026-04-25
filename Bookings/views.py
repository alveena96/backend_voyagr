from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import stripe
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import CreateBookingSerializer, BookingListSerializer
from hotel.models import RoomType, Hotel
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

# =========================
# CREATE BOOKING API
# =========================
class CreateBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateBookingSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        user = request.user

        items_data = data.pop('items')
        billing_data = data.pop('billing')

        payment_method_id = billing_data.get("payment_method_id")

        if not payment_method_id:
            return Response({"error": "Payment method required"}, status=400)

        payment_intent = None
        booking = None

        try:
            # =========================
            # STEP 1: CREATE + CONFIRM INTENT
            # =========================
            payment_intent = stripe.PaymentIntent.create(
                amount=int(billing_data.get('total_amount') * 100),
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method="manual",
                confirm=True,
                capture_method="manual",
                payment_method_types=["card"],
                description="Hotel Booking Authorization"
            )

            # =========================
            # STEP 2: CREATE BOOKING
            # =========================
            with transaction.atomic():

                booking = UserBooking.objects.create(
                    user=user,
                    **data
                )

                for item in items_data:
                    room = RoomType.objects.select_for_update().get(id=item['room'])
                    hotel = Hotel.objects.get(id=item['hotel'])

                    requested_rooms = data['no_of_rooms']
                    requested_persons = data['no_of_people']
                    total_capacity = room.people_per_room * requested_rooms

                    if room.rooms_available < requested_rooms:
                        raise ValidationError("Not enough rooms available")

                    if total_capacity < requested_persons:
                        raise ValidationError("Not enough capacity")

                    room.rooms_available -= requested_rooms
                    room.save()

                    booking.items.create(
                        room=room,
                        hotel=hotel,
                        user=user
                    )
                Billing.objects.create(
                    booking=booking,
                    user=user,
                    stripe_order_id=payment_intent.id,
                    stripe_meta_data = payment_intent.to_dict(),
                    total_amount=billing_data.get('total_amount'),
                    paid=False
                )

        except Exception as e:
            if payment_intent:
                stripe.PaymentIntent.cancel(payment_intent.id)

            return Response({"error": str(e)}, status=400)

        # =========================
        # STEP 3: CAPTURE PAYMENT
        # =========================
        try:
            stripe.PaymentIntent.capture(payment_intent.id)

            Billing.objects.filter(
                stripe_order_id=payment_intent.id
            ).update(paid=True)

        except Exception as e:
            # rollback booking manually
            if booking:
                for item in booking.items.all():
                    room = item.room
                    room.rooms_available += data['no_of_rooms']
                    room.save()

                booking.delete()

            return Response(
                {"error": "Payment failed, booking reversed"},
                status=400
            )

        return Response(
            {
                "message": "Booking successful",
                "booking_id": booking.id,
                "payment_intent": payment_intent.id
            },
            status=201
        )
# =========================
# USER BOOKINGS LIST API
# =========================
class UserBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = UserBooking.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)


# # =========================
# # CANCEL BOOKING API
# # =========================
# =========================
# CANCEL BOOKING API
# only booking_id required
# Uses latest_charge from saved stripe_meta_data
# =========================
import json
class CancelBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        booking = get_object_or_404(
            UserBooking,
            id=pk,
            user=request.user
        )

        billing = booking.billing

        try:
            with transaction.atomic():

                # =========================
                # 1. REFUND STRIPE PAYMENT
                # =========================
                stripe.Refund.create(
                    payment_intent=billing.stripe_order_id
                )

                # =========================
                # 2. RESTORE ROOM STOCK
                # =========================
                for item in booking.items.select_related('room'):
                    room = item.room
                    room.rooms_available += booking.no_of_rooms
                    room.save()

                # =========================
                # 3. DELETE CHILD RECORDS FIRST
                # =========================
                booking.items.all().delete()   # BookingItem delete
                billing.delete()               # Billing delete

                # =========================
                # 4. DELETE BOOKING LAST
                # =========================
                booking.delete()

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

        return Response(
            {"message": "Booking fully cancelled, refunded & cleaned"},
            status=200
        )
    
    
