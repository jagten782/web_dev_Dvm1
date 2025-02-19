
from django.contrib import admin
from .models import Bus,Booking,Wallet,Seatclass,Intermediatestop
from django.http import HttpResponse
import pandas as pd
from .views import export


admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Wallet)
admin.site.register(Seatclass)
admin.site.register(Intermediatestop)


class BookingAdmin(admin.ModelAdmin):
    actions = [export]


admin.site.unregister(Booking)
admin.site.register(Booking,BookingAdmin)




# Register your models here.
