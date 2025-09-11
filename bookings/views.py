from django.shortcuts import render, redirect
from .models import FitnessClass, Booking
from django.contrib import messages
from django.shortcuts import get_object_or_404

def index(request):
    classes = FitnessClass.objects.all()
    return render(request, 'bookings/index.html', {'classes': classes})

def book_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        name = request.POST.get('client_name')
        email = request.POST.get('client_email')

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
            if fitness_class.available_slots > 0:
                Booking.objects.create(
                    fitness_class=fitness_class,
                    client_name=name,
                    client_email=email
                )
                fitness_class.available_slots -= 1
                fitness_class.save()
                messages.success(request, 'Booking successful!')
            else:
                messages.error(request, 'No slots available.')
        except FitnessClass.DoesNotExist:
            messages.error(request, 'Invalid class selected.')
        
        return redirect('book')
    else:
        classes = FitnessClass.objects.all()
        return render(request, 'bookings/book.html', {'classes': classes})

def view_bookings(request):
    bookings = []
    if request.method == 'POST':
        email = request.POST.get('email')
        bookings = Booking.objects.filter(client_email=email)
    return render(request, 'bookings/view_bookings.html', {'bookings': bookings})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    fitness_class = booking.fitness_class
    booking.delete()
    fitness_class.available_slots += 1
    fitness_class.save()
    messages.success(request, 'Booking canceled and slot restored.')
    return redirect('view_bookings')
