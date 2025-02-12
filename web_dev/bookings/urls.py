from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_1, name='login'),
    path('register/', views.register, name='register'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('transaction_history/<int:user_id>/', views.transactions, name='transaction_history'),
    path('my_bookings/<int:user_id>/', views.my_bookings, name='my_bookings'),
    path('search_results/',views.search_results,name='search_results'),
    path('book_form/<int:bus_id>/',views.book_form,name='book_form'),
    path('booking/<int:bus_id>/',views.booking,name='booking'),
    path('pay_confirm/<int:user_id>/',views.pay_confirm,name='payment confirmation'),
    path('add_money/<int:user_id>/',views.add_money,name='add_money'),
    path('redirect_to_dashboard/',views.redirect_to_dashboard,name='redirect_to_dashboard'),
    path('cancel_ticket/<int:user_id>/',views.cancel_ticket,name='cancel_ticket'),
    path('cancel_ticket_1/<int:user_id>/',views.cancel_ticket_1,name='cancel_ticket_1'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('select_class/<int:bus_id>/',views.select_class,name='select_class')
]