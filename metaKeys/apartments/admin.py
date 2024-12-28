from django.contrib import admin
from .models import Apartment, Door, Room, ApartmentInfo

# Register your models here.

admin.site.register(Apartment)
admin.site.register(Door)
admin.site.register(Room)
admin.site.register(ApartmentInfo)

