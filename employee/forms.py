from django import forms
from employee.models import Vehicle

class DeliveryDetailsForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())
    distance = forms.FloatField(label="Distance (km)", min_value=0)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.none(), empty_label="Select Vehicle")

    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        if order:
            # Include available vehicles (not in use) or the currently assigned vehicle
            available_vehicles = Vehicle.objects.filter(in_use=False)
            if order.assigned_vehicle:
                available_vehicles = available_vehicles | Vehicle.objects.filter(id=order.assigned_vehicle.id)
            self.fields['vehicle'].queryset = available_vehicles
            self.fields['vehicle'].initial = order.assigned_vehicle
