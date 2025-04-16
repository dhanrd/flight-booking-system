from django.contrib import admin
from .models import Flight, Aircraft

# Register your models here.
admin.site.register(Flight)
admin.site.register(Aircraft)