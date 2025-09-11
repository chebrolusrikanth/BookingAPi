from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('book/', views.book_class, name='book'),
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
