from django.db import models
from django.contrib.auth.models import User

class ClassType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class FitnessClass(models.Model):
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.class_type.name} with {self.instructor} on {self.date} at {self.time}"

    def spots_remaining(self):
        return self.capacity - self.booking_set.count()

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class}"