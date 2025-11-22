from django.db import models

class Vehicle(models.Model):
    TYPE_CHOICES = (
        ('van', 'Van'),
        ('motorcycle', 'Motorcycle'),
        ('truck', 'Truck'),
        ('mini_van', 'Mini Van'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    plate_number = models.CharField(max_length=20)
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_type_display()} - {self.plate_number}"
