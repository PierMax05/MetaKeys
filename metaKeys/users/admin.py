from django.contrib import admin
from .models import Profile, CheckInProfile, Guest, BillingInfo

# Register your models here.

admin.site.register(Profile)
admin.site.register(CheckInProfile)
admin.site.register(Guest)
admin.site.register(BillingInfo)

