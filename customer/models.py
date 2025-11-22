from django.db import models
from django.conf import settings
from employee.models import Vehicle

class Order(models.Model):
    PERISHABILITY = (
        ('yes', 'Perishable'),
        ('no', 'Not Perishable'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    is_perishable = models.CharField(max_length=3, choices=PERISHABILITY)
    weight = models.FloatField()
    price = models.FloatField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_orders')
    assigned_vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='Pending')
    customer_verified = models.BooleanField(default=False)  # New field for customer verification
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_perishable == 'yes':
            if self.weight <= 10:
                self.price = 1000
            elif self.weight <= 20:
                self.price = 5000
            else:
                self.price = 10000
        else:
            if self.weight <= 10:
                self.price = 500
            elif self.weight <= 20:
                self.price = 2500
            else:
                self.price = 5000
        super().save(*args, **kwargs)

    @property
    def employee_contact(self):
        if self.assigned_to:
            return self.assigned_to.email or self.assigned_to.username
        return None

    @property
    def eta(self):
        # Placeholder for ETA calculation or field
        return getattr(self, '_eta', '-')

    _distance_away = models.FloatField(null=True, blank=True)

    @property
    def distance_away(self):
        return self._distance_away or '-'

    @distance_away.setter
    def distance_away(self, value):
        self._distance_away = value
