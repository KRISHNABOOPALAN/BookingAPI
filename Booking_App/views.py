import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from .models import FitnessClass, Booking
from .forms import BookingForm, RegisterForm
from django.conf import settings

# Setup logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('booking.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def Home(request):
    logger.info("Home page accessed")
    classes = FitnessClass.objects.all()
    return render(request, 'Home.html', {'classes': classes})

@login_required
def Book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    full = fitness_class.spots_remaining() <= 0
    message = None

    if request.method == 'POST':
        if full:
            message = "Sorry, this class is fully booked."
            logger.warning(f"Booking failed: Class full (ID: {class_id}) - User: {request.user.username}")
        else:
            Booking.objects.create(fitness_class=fitness_class, user=request.user)
            logger.info(f"Booking confirmed for {request.user.username} in class ID {class_id}")
            message = "Your booking is confirmed! A confirmation email has been sent."
            try:
                send_mail(
                    subject='Booking Confirmation',
                    message=f"Hi {request.user.username},\n\nYou have successfully booked a spot for {fitness_class.class_type.name} on {fitness_class.date} at {fitness_class.time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                )
                logger.info(f"Email sent to {request.user.email} for class ID {class_id}")
            except Exception as e:
                logger.error(f"Failed to send email to {request.user.email}: {e}")

    return render(request, 'Book_class.html', {
        'fitness_class': fitness_class,
        'full': full,
        'message': message,
    })

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered: {user.username}")
            return redirect('Home')
        else:
            logger.warning("User registration failed: Invalid form submission")
    else:
        form = RegisterForm()
    return render(request, 'Register.html', {'form': form})

def Custom_logout(request):
    logger.info(f"User logged out: {request.user.username}")
    logout(request)
    return redirect('Home')
