from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate  
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import get_object_or_404
from .models import Bus, Booking,Wallet,Seatclass,Intermediatestop,Route,Day
from decimal import Decimal
from datetime import datetime,timedelta
from django.utils import timezone
import random
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import pandas as pd
from django.contrib import admin

def register(request):
    print(request)
    if request.method == 'POST':
        uname=request.POST.get('username')
        uemail=request.POST.get('email')
        upass=request.POST.get('Password')
        request.session['username']=uname
        request.session['email']=uemail
        request.session['Password']=upass
        if User.objects.filter(username=uname).exists():
            return render(request, "bookings/register.html", {"error": "Username already taken!"})
        request.session['user_email'] = uemail
        print(uemail)
        if 'send_otp' in request.POST:
         r_email=request.session['user_email']
         send_otp_email(request,r_email)
        if 'verify_otp' in request.POST:
         otp=request.session['otp']
         i_otp=request.POST.get('ootp')
         if ((int(otp)-int(i_otp))==0):
             user_1=User.objects.create_user(uname,uemail,upass)
             user_1.save()
             print('created user')
             user_1.is_staff=True
             wallet, created = Wallet.objects.get_or_create(user=request.user)
             return render(request,"bookings/login.html",{'message':'CREATED ACCOUNT SUCCESSFULLY!'})
         else:
             return render(request,'bookings/register.html',{'message_1':'You have entered wrong otp!!!'})
        else:
            return render(request,'bookings/register.html',{'message':'show otp','username':uname,'email':uemail,'password':upass}) 
    return  render(request, "bookings/register.html")

def login_1(request):
    print(User.objects.all())
    print(Bus.objects.all())
    if request.method== 'POST':
         uname=request.POST.get('username')
         upass=request.POST.get('Password')
         user=authenticate(request,username=uname,password=upass)
         if user is not None:
              login(request,user)
              buses=Bus.objects.all()
              wallet, created = Wallet.objects.get_or_create(user=request.user)
              return render(request,"bookings/dashboard.html",{'buses':buses,'balance':wallet.balance})
         else:
            return render(request, "bookings/login.html", {"error": "Invalid username or password"})

    return render(request, "bookings/login.html") 


def book_ticket(request):
    return render(request,"bookings/book_ticket.html")

 
def my_bookings(request,user_id):
  bookings= Booking.objects.filter(user=request.user,status='booked')
  return render(request,"bookings/my_bookings.html",{'bookings':bookings,'user_id':user_id})


def transactions(request,user_id):
    return render(request,"bookings/book_ticket.html")


def search_results(request):
    if request.method=='POST':
         source=request.POST.get('Source')
         request.session['source']=source
         dest=request.POST.get('Destination')
         request.session['Destination']=dest
         date=request.POST.get('date')
         request.session['date']=date
         if date:
             date = datetime.strptime(date, '%Y-%m-%d')
             day_of_week = date.strftime('%A')
             request.session['day']=day_of_week
             buses = Bus.objects.all()
             time={}
             days = Day.objects.filter(day_of_week=day_of_week)
             buses_1=[]
             for bus in buses:
                print("loop starts")
                stops = Route.objects.filter(bus=bus)
                print(stops)
                for stop in stops:
                    s=-1
                    k=-1
                    for intermediate_stop in stop.intermediate_stops.all():
                         if str(intermediate_stop.location) == source:
                              s=intermediate_stop.stop_order
                              t=intermediate_stop.arrival_time
                         elif str(intermediate_stop.location) == dest:
                            k=intermediate_stop.stop_order
                         if s<k and s>=0 and k>0:    
                                n=bus.name
                                buses_1.append(n)
                                time[n]=t
             bus=Bus.objects.filter(name__in=buses_1).filter(routes__day__in=days)                           
             days = Day.objects.filter(day_of_week=day_of_week)
             formatted_time = {bus: arrival_time.strftime('%H:%M') for bus, arrival_time in time.items()} 
             request.session['time']=formatted_time 
             print(f'I am sending this to html file f{formatted_time}')  
             print(f'Buses contains this : {buses_1}')      
             if buses.exists():
                  return render(request,"bookings/search.html",{'buses':bus,'time':formatted_time})
             else:
                 return render(request, "bookings/book_ticket.html", {"error": "No buses found on this day."})
         else:
            return render(request, "bookings/book_ticket.html", {"error": "Please provide a valid date."})
    else:
     return render(request,"bookings/book_ticket.html",{"error":"No bus found"})




def book_form(request,bus_id):
    return render(request,'bookings/book_form.html',{'bus_id':bus_id})




def select_class(request,bus_id):
    source=request.session.get('source')
    dest=request.session.get('Destination')
    date=request.session.get('date')
    fare={}
    buses=Bus.objects.filter(id=bus_id)
    s_1=(Intermediatestop.objects.filter(location__location=source).distinct())
    s_2=(Intermediatestop.objects.filter(location__location=dest).distinct())
    print(s_1)
    print("\n")
    print(s_2)
    if  s_1.exists():
        multi_1=s_1.first().fare_multiplier
    if  s_2.exists():
         multi_2=s_2.first().fare_multiplier
    print("Debugging :\n")     
    day=request.session.get('day')
    for bus in buses:    
         for t in bus.seat_classes.all():
             print(t)
             for d in t.day.all():
                 print(d)
                 print(f"{d}=={day}")
                 if str(d)==str(day): 
                   print("accmomp")
                   print(t)
                   fare_calc=t.price_class*(multi_1-multi_2)
                   fare[t.name]=fare_calc
    if request.method=="POST":
        if 'a' in request.POST:
              ft=request.POST.get('a')
              print(ft)
              request.session['fare']=ft
              for a,b in fare.items():
                  print(f'{b}=={ft}')
                  if (float(b) == float(ft)):
                      clas=a
              request.session['travel_class']=clas        
              dict=avail_seats(bus_id,request,clas)
              for a,b in dict.items():
                 if (a==f'{source} to {dest}'):
                     if b>0: 
                         print(f'Seats available are : {b}')
                         request.session['avail_seats']=b
                         return render(request,'bookings/book.html',{'bus_id':bus_id})
                     else:
                         return render(request,'bookings/select_class.html',{'fare':fare,'bus':bus,'error':'no tickets available in this class'})      
        else:
             return render(request,'bookings/select_class.html',{'fare':fare,'bus':bus})
    else:
        return render(request,'bookings/select_class.html',{'fare':fare,'bus':bus})

            

def booking(request, bus_id):
    if request.method == "POST":
        bus = get_object_or_404(Bus, id=bus_id)
        wallet,created = Wallet.objects.get_or_create(user=request.user)
        print(request.session.get('avail_seats'))
        seats=int(request.session.get('avail_seats'))
        source=request.session.get('source')
        dest=request.session.get('Destination')
        print(f'Balance before :{wallet.balance}')
        if 'add' in request.POST:
            num_tickets = int(request.POST.get('tickets', 1))
            
            return render(request, 'bookings/book.html', {
                'range': range(num_tickets),
                'bus_id': bus_id
            })
        elif 'payments' in request.POST:
            num_tickets = int(request.POST.get('tickets', 1))

            if seats < num_tickets:
                return render(request, 'bookings/book.html', {
                    'bus_id': bus_id,
                    'error': "Not enough seats available.",
                    'range': range(num_tickets)
                })
            time_1={}
            time_1=request.session.get('time')
            print(time_1)
            for a,b in time_1.items():
                if (a==bus.name):
                    print(f'{a}---->{b}')

                    time_ofdepart=b
            for i in range(num_tickets):
                name = request.POST.get(f'pass_name_{i}')
                email = request.POST.get(f'email_{i}')
                date = request.session.get('date')
                journey_date = datetime.strptime(date, '%Y-%m-%d').date()
                print(journey_date)
                fare=request.session.get('fare')
                cost=num_tickets*fare
                print(f'Cost is {cost}')
                cost=Decimal(cost)
                if wallet.balance>=cost:
                    wallet.withdraw(cost)
                    if name and email:
                         Booking.objects.create(
                        user=request.user,
                        bus=bus,
                        passenger_name=name,
                        passenger_email=email,
                        num_tickets=1,
                        journey_date=journey_date,
                        boarding=source,
                        deboarding=dest,
                        time=time_ofdepart,
                        travelling_class=request.session.get('travel_class'),
                        cost=cost
                    )
                    bus.save()
                    print(f'Ticket booked for: {name}')
                    seat=Seatclass.objects.get(name=request.session.get('travel_class'))
                    seat.update_seats_afterbooking(num_tickets,bus_id)

                    print(f'Balance after booking ticket is: {wallet.balance}')
                    return render(request, 'bookings/payment.html', {
                 'user_id': request.user.id,
                 'num_tickets':num_tickets,
                 'cost':(num_tickets*fare),
                 'balance':wallet.balance
                        })
                else:
                    return render(request, 'bookings/add_money.html', {'user_id': request.user.id,'error':'insufficient balance'})
        else:
            return render(request, 'bookings/book.html', {'bus_id':bus_id})
        
    else:
        return render(request, 'bookings/book.html', {'bus_id':bus_id})
    

def add_money(request,user_id):
    if request.method=='POST':
        money=request.POST.get('add')
        if money:
            try:
                money_decimal = Decimal(money.strip())
                wallet, created = Wallet.objects.get_or_create(user=request.user)
                if(money_decimal>0):
                 wallet.deposit(money_decimal)
                 print(f"update balance is:{wallet.balance}")
                 return render(request, 'bookings/dashboard.html',{'balance':wallet.balance})
                else:
                    
                 error_message = "Invalid amount entered. Please enter a valid number."
                 return render(request, 'bookings/add_money.html', {'error': error_message})

            except :
                error_message = "Invalid amount entered. Please enter a valid number."
                return render(request, 'bookings/add_money.html', {'error': error_message})
        else:
            error_message = "Please enter a valid amount."
            return render(request, 'bookings/add_money.html', {'error': error_message})
    return render(request, 'bookings/add_money.html')  



def redirect_to_dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request,'bookings/dashboard.html',{'balance':wallet.balance})

def dashboard(request):
    return render(request,'bookings/dashboard.html')



def pay_confirm(request,user_id):
    if request.method=='POST':
        return render(request,"bookings/dashboard.html")



def cancel_ticket(request,user_id):
    bookings= Booking.objects.filter(user=user_id,status='booked')
    now = timezone.now() 
    future_bookings = []
    for booking in bookings:
         date_time = datetime.combine(booking.journey_date, booking.time)
         now_min = (now.hour * 60) + now.minute
         depart_min = (date_time.hour * 60) + date_time.minute
         if((now.month < date_time.month) or ((now.month==date_time.month)and(now.day < date_time.day)) or ((now.month==date_time.month)and(now.day==date_time.day)and(depart_min - now_min) >= 360)):
                 print(booking)
                 print(now)
                 future_bookings.append(booking)
    if request.method=='POST':
        wallet,created = Wallet.objects.get_or_create(user=request.user)
        print(f'Balance before cancelling ticket is :{wallet.balance}')
        cancel_booking_ids = request.POST.getlist('cancel_booking')
        if cancel_booking_ids:
            booking_tocancel=Booking.objects.filter(id__in=cancel_booking_ids)
            for booking in booking_tocancel:
                booking.cancel_booking()
                seat=Seatclass.objects.get(name=booking.travelling_class)
                seat.update_seats_aftercancellation(1,booking.bus.id)
                wallet.deposit(booking.cost)
            print(f'Balance after cancelling ticket is :{wallet.balance}')    
        return render(request,'bookings/dashboard.html',{'bookings':future_bookings,'message':'Successfully cancelled ticket!!!','balance':wallet.balance})
    else:
        return render(request,'bookings/cancel_ticket.html',{'bookings':future_bookings})
    



def cancel_ticket_1(request,user_id):
    
    bookings= Booking.objects.filter(user=user_id,status='booked')
    now = timezone.now() 
    future_bookings = []
    for booking in bookings:
         date_time = datetime.combine(booking.journey_date, booking.time)
         now_min = (now.hour * 60) + now.minute
         depart_min = (date_time.hour * 60) + date_time.minute
         if((now.month < date_time.month) or ((now.month==date_time.month)and(now.day < date_time.day)) or ((now.month==date_time.month)and(now.day==date_time.day)and(depart_min - now_min) >= 360)):
                 print(booking)
                 print(now)
                 future_bookings.append(booking)
    return render(request,'bookings/cancel_ticket.html',{'bookings':future_bookings})             



def send_otp_email(request,user_email):
    otp=random.randint(100000, 999999)
    subject = 'Your OTP for Bus Booking'
    message = f'Your One-Time Password (OTP) is: {otp}'
    print(otp)
    request.session['otp'] = otp
    from_email = settings.EMAIL_HOST_USER
    print(f'Email sent to {user_email}')
    send_mail(subject, message, from_email,[user_email])


def avail_seats(bus_id,request,seat_type):
    bus=Bus.objects.get(id=bus_id)
    book=Booking.objects.filter(bus=bus).filter(status='booked')
    dict=[] 
    dict_1={}
    day=request.session.get('day')
    for r in bus.routes.all():
        dict=r.map(day)
    length=len(dict) 
    p=0
    q=0
    le=Seatclass.objects.get(bus=bus,name=seat_type)
    l=le.total_seats
    dict_2={}
    arr_1=[]
    if book:
     for i in range(0,length):
         for a in range(1,length):
             for b in book:
                 p=0
                 if b.deboarding==str(dict[a]) and  b.boarding==str(dict[i]) and i<a:
                     p=p+1
                     for j in range(0,length):
                         for k in range(0,length):
                             if k>j and (j<a) :
                                 q = dict_1.get(f"{dict[j]} to {dict[k]}", 0) 
                                 if q==0:
                                     dict_1[f"{dict[j]} to {dict[k]}"]=l-p
                                 else:
                                     dict_1[f"{dict[j]} to {dict[k]}"]=q-p
                               
                 else:
                     for j in range(0,a):
                         for k in range(1,a+1):
                           if k>j  :
                               q = dict_1.get(f"{dict[j]} to {dict[k]}", 0) 
                               if q==0:
                                  dict_1[f"{dict[j]} to {dict[k]}"]=l
                               else:
                                 dict_1[f"{dict[j]} to {dict[k]}"]=q                           
    else:
        for i in range(1,length):
             for j in range(0,i):
                 dict_1[f"{dict[j]} to {dict[i]}"]=l
    return(dict_1)



@admin.action(description='Export all bookings to Excel')
def export(modeladmin, request,queryset):
    bookings = queryset

    bookings =Booking.objects.all()
    data=[]
    for booking in bookings:
        data.append({
            'user': booking.user.username,
            'bus': booking.bus.name,
            'num_tickets': booking.num_tickets,
            'passenger_name': booking.passenger_name,
            'passenger_email': booking.passenger_email,
            'status': booking.status,
            'journey_date': booking.journey_date,
            'boarding': booking.boarding,
            'deboarding': booking.deboarding,
            'time': booking.time,
            'travelling_class': booking.travelling_class
        })
    read = pd.DataFrame(data)
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    response['Content-Disposition'] = 'attachment; filename="all_bookings.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        read.to_excel(writer, index=False, sheet_name='Bookings')

    return response








# Create your views here.
