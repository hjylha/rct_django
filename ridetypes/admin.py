from django.contrib import admin

from .models import RideType, RideName

# Register your models here.
admin.site.register(RideType)
admin.site.register(RideName)
