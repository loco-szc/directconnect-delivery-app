from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customer.models import Order
from employee.models import Vehicle
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.timezone import now
from .forms import DeliveryDetailsForm

@login_required
def employee_dashboard(request):
    user = request.user
    employee_name = user.get_full_name() or user.username

    # Count assigned orders by status
    assigned_orders = Order.objects.filter(assigned_to=user)
    deliveries_today = assigned_orders.filter(status='delivered', created_at__date=now().date()).count()
    pending_deliveries = assigned_orders.filter(status='assigned').count()

    context = {
        'employee_name': employee_name,
        'deliveries_today': deliveries_today,
        'pending_deliveries': pending_deliveries,
        'assigned_orders': assigned_orders,
    }
    return render(request, 'employee/dashboard.html', context)

@login_required
def delivery_details_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, assigned_to=request.user)
    if request.method == 'POST':
        form = DeliveryDetailsForm(request.POST, order=order)
        if form.is_valid():
            distance = form.cleaned_data['distance']
            vehicle = form.cleaned_data['vehicle']
            # Handle vehicle reassignment
            if order.assigned_vehicle and order.assigned_vehicle != vehicle:
                # Release the previously assigned vehicle
                order.assigned_vehicle.in_use = False
                order.assigned_vehicle.save()
            # Assign new vehicle and mark as in use
            if vehicle:
                vehicle.in_use = True
                vehicle.save()
            # Save distance and assign vehicle to order
            order.distance_away = distance
            order.assigned_vehicle = vehicle
            order.save()
            messages.success(request, 'Delivery details updated successfully.')
            return redirect('employee:dashboard')
    else:
        form = DeliveryDetailsForm(initial={'order_id': order.id}, order=order)
    return render(request, 'employee/delivery_details.html', {'form': form, 'order': order})

@login_required
def assigned_orders(request):
    orders = Order.objects.filter(assigned_to=request.user)
    return render(request, 'employee/assigned_orders.html', {'orders': orders})

@login_required
def unassigned_orders(request):
    # List all orders not assigned to any employee and pending status
    orders = Order.objects.filter(assigned_to__isnull=True, status='pending')

    # Get available vehicles
    vehicles = Vehicle.objects.filter(in_use=False)

    context = {
        'orders': orders,
        'vehicles': vehicles,
    }
    return render(request, 'employee/unassigned_orders.html', context)

@login_required
@require_POST
def request_assignment(request):
    order_id = request.POST.get('order_id')
    vehicle_id = request.POST.get('vehicle_id')
    try:
        order = Order.objects.get(id=order_id, assigned_to__isnull=True)
        vehicle = Vehicle.objects.get(id=vehicle_id, in_use=False)
    except Order.DoesNotExist:
        messages.error(request, "Order not found or already assigned.")
        return redirect('employee:unassigned_orders')
    except Vehicle.DoesNotExist:
        messages.error(request, "Vehicle not available.")
        return redirect('employee:unassigned_orders')

    # Mark vehicle as in use
    vehicle.in_use = True
    vehicle.save()

    # Assign order to current employee and vehicle
    order.assigned_to = request.user
    order.assigned_vehicle = vehicle
    order.status = 'assigned'
    order.save()

    messages.success(request, f"Order {order.id} assigned to you with vehicle {vehicle.type}.")
    return redirect('employee:assigned_orders')

@login_required
@require_POST
def start_delivery(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id, assigned_to=request.user, status='assigned')
    except Order.DoesNotExist:
        messages.error(request, "Order not found or cannot be started.")
        return redirect('employee:assigned_orders')

    order.status = 'in_transit'
    order.save()
    messages.success(request, f"Order {order.id} marked as In Transit.")
    return redirect('employee:assigned_orders')

@login_required
@require_POST
def complete_delivery(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id, assigned_to=request.user, status='in_transit')
    except Order.DoesNotExist:
        messages.error(request, "Order not found or cannot be completed.")
        return redirect('employee:assigned_orders')

    order.status = 'delivered'
    order.save()
    messages.success(request, f"Order {order.id} marked as Delivered.")
    return redirect('employee:assigned_orders')

@login_required
def employee_profile(request):
    user = request.user
    employee_name = user.get_full_name() or user.username
    context = {
        'employee_name': employee_name,
        'employee_user': user,
    }
    return render(request, 'employee/profile.html', context)
