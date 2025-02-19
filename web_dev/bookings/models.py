from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.http import HttpResponse
import pandas as pd





class Bus(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    duration=models.DecimalField(max_digits=4, decimal_places=2,default=0.0)
    running_days = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name
    


class Seatclass(models.Model):
    bus = models.ForeignKey(Bus, related_name='seat_classes', on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)  
    price_class = models.DecimalField(max_digits=5, decimal_places=2)  
    available_seats = models.IntegerField()  
    def __str__(self):
     return self.name
    
    def update_seats_afterbooking(self,num_tickets,bus_id):
        b=Bus.objects.get(id=bus_id)
        if self.bus != b:
            raise ValueError("The seat class does not belong to the given bus.")
        if self.available_seats >= num_tickets:
            
            self.available_seats -= num_tickets
            self.save()

    def update_seats_aftercancellation(self,num_tickets,bus_id):
        b=Bus.objects.get(id=bus_id)
        if self.bus != b:
            raise ValueError("The seat class does not belong to the given bus.")
        else:
            self.available_seats += num_tickets
            self.save()
             
        



class Intermediatestop(models.Model):
    bus = models.ForeignKey(Bus, related_name='intermediate_stops', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    stop_order = models.IntegerField()  
    arrival_time = models.TimeField(blank=True, null=True) 
    fare_multiplier=models.DecimalField(max_digits=5,decimal_places=4,default=0.0) 
    def __str__(self):
        return f' ({self.location})'


    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)
    passenger_name=models.CharField(max_length=100)
    passenger_email=models.EmailField(max_length=100)
    booking_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=10, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')], default='booked')
    journey_date=models.DateField(default=timezone.now)
    boarding=models.CharField(max_length=100,default='enter')
    deboarding=models.CharField(max_length=100,default='enter')
    time=models.TimeField(default='00:00:00')
    travelling_class=models.CharField(max_length=100,default='none')
    cost=models.IntegerField(default='0')

    def __str__(self):
        return f"{self.user.username} - {self.bus.name} ({self.num_tickets} tickets)"
    def cancel_booking(self):
        if self.status == 'cancelled':
            raise ValueError("This booking has already been cancelled.")
        self.status = 'cancelled'
        self.save()



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"
    












    

# Create your models here.
