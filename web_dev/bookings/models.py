from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.http import HttpResponse
import pandas as pd



class Day(models.Model):
    DAY_CHOICES = [
         ('Monday', "Monday"),
        ('Tuesday', "Tuesday"),
        ('Wednesday', "Wednesday"),
        ('Thursday', "Thursday"),
        ('Friday', "Friday"),
        ('Saturday', "Saturday"),
        ('Sunday', "Sunday")
    ]

    day_of_week = models.CharField(
        max_length=20,
        unique=True,
        choices=DAY_CHOICES,
        default='Monday'
    )

    def __str__(self):
        return dict(self.DAY_CHOICES).get(self.day_of_week, self.day_of_week)

class Bus(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    departure_time = models.TimeField()
    duration=models.DecimalField(max_digits=4, decimal_places=2,default=0.0)
    running_days =models.ManyToManyField(Day)
    def __str__(self):
        return self.name
    

class Locations(models.Model):
    Loc=[
        ("Pilani","Pilani"),
        ("Loharu","Loharu"),
        ("Delhi","Delhi"),
        ("Gurugram","Gurugram"),
        ("Rewari","Rewari"),
        ("Chandigrah","Chandigarh"),
        ("Chirawa","Chirawa"),
        ("Ghaziabad","Ghaziabad"),
        ("Agra","Agra"),
        ("Noida","Noida"),
        ("Shikohabad","Shikohabad"),
        ("Etawah","Etawah"),
        ("Kanour","Kanpur"),
        ("Lucknow","Lucknow")
    ]
    location=models.CharField(max_length=25,choices=Loc)  
    def __str__(self):
        return self.location  
    


class Seatclass(models.Model):
    bus = models.ForeignKey(Bus, related_name='seat_classes', on_delete=models.CASCADE,null=True)
    day=models.ManyToManyField(Day)
    name = models.CharField(max_length=50)  
    price_class = models.DecimalField(max_digits=5, decimal_places=2)  
    total_seats=models.IntegerField(default=0)
    available_seats = models.IntegerField()  
    def __str__(self):
     return (f'{self.name}')
    
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
             
class Route(models.Model):
    bus = models.ForeignKey(Bus,related_name='routes',on_delete=models.CASCADE)
    day=models.ManyToManyField(Day)
    def __str__(self):
        loc=[]
        for s in self.intermediate_stops.all():
          loc.append(s.location)
        return str(loc) 

    def map(self,d):
        print(f' Bus is in models.py :{self.bus}')
        print(f"day which I recieved here is : {d}")
        l=[]
        i=0
        for da in self.day.all():
            print(f"{da}=={d}")
            if str(da)==str(d):
                for s in self.intermediate_stops.all():
                    print(s)
                    l.append(s.location)
        return (l)



class Intermediatestop(models.Model):
    route=models.ForeignKey(Route,on_delete=models.CASCADE,related_name='intermediate_stops',default='1')
    location=models.ForeignKey(Locations,on_delete=models.CASCADE,default=1)
    stop_order = models.IntegerField()  
    arrival_time = models.TimeField(blank=True,null=True) 
    fare_multiplier=models.DecimalField(max_digits=5,decimal_places=4,default=0.0) 
    def __str__(self):
        return (str(self.location))


    
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
