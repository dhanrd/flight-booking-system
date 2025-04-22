from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Admin, Flight, Aircraft, Booking
from django.http import HttpRequest

# Register your models here.
class UserAdmin(BaseUserAdmin):
  model = User
  
  # Editing a new user in admin
  fieldsets = (
      (_('Login Information'), {"fields": ('email', 'password')}),
      (_('Personal Information'), {"fields" : ('first_name', 'last_name', 'date_of_birth', 'phone_number')}),
      (_('Permissions'), {"fields" : ('is_active', 'is_admin', 'is_staff', 'is_superuser')}),
      (_('Important dates'), {"fields" : ('last_login',)})
  )
  
  list_display = ('first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_admin')
  search_fields = ('email', 'phone_number')
  ordering = ('first_name', 'last_name')
  
class SystemAdmin(admin.ModelAdmin):
  list_display = ('AdminID','authorization_level',)
  search_display = ('authorization_level',)
  
class FlightAdmin(admin.ModelAdmin):
  list_display = ('flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_id')
  search_fields = ('flight_number', 'departure_airport', 'arrival_airport')
  ordering = ('departure_time',)

class AircraftAdmin(admin.ModelAdmin):
  list_display = ('model', 'capacity')
 
class BookingAdmin(admin.ModelAdmin):
  list_display = ('booking_id', 'passenger_id', 'flight_id', 'booking_date', 'booking_status')
  
  def get_queryset(self, request: HttpRequest):
    qs = super().get_queryset(request) # retrieve all Booking objects
  
    # If the logged in user is a superuser, return all the user bookings
    if request.user.is_superuser:
      return qs

    # Return the bookings associated with the logged in admin (not superuser)
    # Return an empty set if the admin does not exist
    try:
      admin_user = Admin.objects.get(AdminID=request.user)
      return qs.filter(admin_id=admin_user)
    except:
      return qs.none()
      
  
admin.site.register(User, UserAdmin)
admin.site.register(Admin, SystemAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Booking, BookingAdmin)