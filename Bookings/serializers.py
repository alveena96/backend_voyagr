from rest_framework import serializers
from .models import UserBooking, BookingItem, Billing
from hotel.models import RoomType, Hotel


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ['id', 'room', 'hotel']


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = [
            'stripe_order_id',  # your custom payment ID
            'total_amount',
            'paid'
        ]


class CreateBookingSerializer(serializers.Serializer):
    check_in_date = serializers.DateField()
    check_out_date = serializers.DateField()
    no_of_people = serializers.IntegerField()
    no_of_rooms = serializers.IntegerField()

    items = serializers.ListField(
        child=serializers.DictField()
    )

    billing = serializers.DictField()

    def create(self, validated_data):
        user = self.context['request'].user

        items_data = validated_data.pop('items')
        billing_data = validated_data.pop('billing')

        # Create booking
        booking = UserBooking.objects.create(
            user=user,
            **validated_data
        )

        # Create booking items
        for item in items_data:
            room = RoomType.objects.get(id=item['room'])
            hotel = Hotel.objects.get(id=item['hotel'])

            BookingItem.objects.create(
                booking=booking,
                room=room,
                hotel=hotel,
                user=user
            )

        # Create billing
        Billing.objects.create(
            booking=booking,
            user=user,
            stripe_order_id=billing_data.get('payment_id'),
            total_amount=billing_data.get('total_amount'),
            paid=billing_data.get('paid', True)
        )

        return booking


class BookingItemDetailSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()
    hotel = serializers.StringRelatedField()

    class Meta:
        model = BookingItem
        fields = ['id', 'room', 'hotel']


class BookingListSerializer(serializers.ModelSerializer):
    items = BookingItemDetailSerializer(many=True)
    billing = BillingSerializer()

    class Meta:
        model = UserBooking
        fields = [
            'id',
            'check_in_date',
            'check_out_date',
            'no_of_people',
            'no_of_rooms',
            'created_at',
            'items',
            'billing'
        ]