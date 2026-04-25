from django.contrib import admin
from .models import *


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'price_range')
    search_fields = ('name', 'location')  # ✅ REQUIRED
    inlines = [PictureInline]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')



@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'room_type', 'price')
    search_fields = ('room_type', 'hotel__name')  # ✅ REQUIRED..


