
from django.contrib import admin
from .models import Bus,Booking,Wallet,Seatclass,Intermediatestop,Locations,Day,Route
from django.http import HttpResponse
import pandas as pd
from .views import export


admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Wallet)
admin.site.register(Seatclass)



class StopInline(admin.TabularInline):
    model=Intermediatestop
    extra = 1
    fields = ('location', 'arrival_time','stop_order','fare_multiplier')





class BookingAdmin(admin.ModelAdmin):
    actions = [export]
    
class RouteAdmin(admin.ModelAdmin):
    inlines = [StopInline]    



admin.site.unregister(Booking)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Route,RouteAdmin)
admin.site.register(Locations)
admin.site.register(Day)





# Register your models here.
