from django.contrib import admin
from .models import UserBooking, BookingItem, Billing


# 🔹 Inline for Booking Items (inside UserBooking)
class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0
    autocomplete_fields = ['room', 'hotel', 'user']


# 🔹 UserBooking Admin
@admin.register(UserBooking)
class UserBookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'check_in_date',
        'check_out_date',
        'no_of_people',
        'no_of_rooms',
        'created_at'
    )
    list_filter = ('check_in_date', 'check_out_date', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    inlines = [BookingItemInline]

    fieldsets = (
        ("User Info", {
            'fields': ('user',)
        }),
        ("Booking Details", {
            'fields': (
                'check_in_date',
                'check_out_date',
                'no_of_people',
                'no_of_rooms',
            )
        }),
        ("Metadata", {
            'fields': ('created_at',),
        }),
    )

    readonly_fields = ('created_at',)


# 🔹 BookingItem Admin
@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'user', 'hotel', 'room')
    list_filter = ('hotel', 'room')
    search_fields = (
        'booking__id',
        'user__username',
        'hotel__name'
    )
    autocomplete_fields = ['booking', 'room', 'hotel', 'user']


# 🔹 Billing Admin
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booking',
        'user',
        'total_amount',
        'paid',
        'stripe_order_id',
        'created_at'
    )
    list_filter = ('paid', 'created_at')
    search_fields = (
        'booking__id',
        'user__username',
        'stripe_order_id'
    )
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Payment Info", {
            'fields': (
                'booking',
                'user',
                'stripe_order_id',
                'total_amount',
                'paid',
                'stripe_meta_data'
            )
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )