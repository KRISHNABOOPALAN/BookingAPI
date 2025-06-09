import logging
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking

# Set up logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('booking.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Serializers
class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


# ViewSets
class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Fetched class list")
        return super().list(request, *args, **kwargs)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        client_email = data.get('client_email')
        class_id = data.get('fitness_class')

        logger.info(f"Booking attempt: {client_email}")

        if not client_email or not class_id:
            return Response({"error": "client_email and fitness_class are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.contrib.auth.models import User
            user, _ = User.objects.get_or_create(username=client_email, defaults={"email": client_email})
            fitness_class = FitnessClass.objects.get(id=class_id)

            if fitness_class.spots_remaining() <= 0:
                logger.warning(f"No available slots for class ID {class_id}")
                return Response({"error": "No available slots"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the booking
            Booking.objects.create(fitness_class=fitness_class, user=user)
            logger.info(f"Booking confirmed for {client_email} in class {fitness_class}")

            return Response({
                "message": "Booking successful",
                "class": str(fitness_class),
                "user": user.username,
                "spots_left": fitness_class.spots_remaining()
            }, status=status.HTTP_201_CREATED)

        except FitnessClass.DoesNotExist:
            logger.error(f"FitnessClass with id {class_id} not found")
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error during booking")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request, *args, **kwargs):
        email = request.query_params.get("client_email")
        if email:
            logger.info(f"Fetching bookings for email: {email}")
        return super().list(request, *args, **kwargs)
