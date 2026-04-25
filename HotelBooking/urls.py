
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('api/user/',include("users.urls")),
    path('api/hotels/',include("hotel.urls")),
    path('api/bookings/',include("Bookings.urls")),
    path('admin/', admin.site.urls),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "Voyagr Admin"
admin.site.site_title = "Voyagr Booking Admin"
admin.site.index_title = "Dashboard"