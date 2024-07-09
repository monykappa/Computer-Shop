from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DeliveryAssignment
from orders.models import OrderStatus
from .forms import *
from userprofile.models import *
from django.db.models import Prefetch


@login_required
def delivery_guy_dashboard(request):
    assignments = (
        DeliveryAssignment.objects.filter(
            delivery_staff__user=request.user, order__status=OrderStatus.PENDING
        )
        .select_related("order", "order__user")
        .prefetch_related(
            Prefetch(
                "order__user__address_set",
                queryset=Address.objects.all(),
                to_attr="addresses",
            )
        )
    )

    return render(request, "delivery/dashboard.html", {"assignments": assignments})


@login_required
def mark_delivery_complete(request, assignment_id):
    assignment = get_object_or_404(
        DeliveryAssignment, id=assignment_id, delivery_staff__user=request.user
    )

    if request.method == "POST":
        try:
            assignment.mark_completed()
            messages.success(
                request, f"Order #{assignment.order.id} has been marked as delivered and you are now available for new deliveries."
            )
        except Exception as e:
            messages.error(request, f"An error occurred while marking the delivery as complete: {str(e)}")
        return redirect("delivery:delivery_guy_dashboard")

    return render(
        request, "delivery/confirm_completion.html", {"assignment": assignment}
    )

def create_delivery_staff(request):
    if request.method == "POST":
        form = DeliveryStaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "dashboard:delivery_staff_list"
            )  # Redirect to a page listing all delivery staff members
    else:
        form = DeliveryStaffCreationForm()
    return render(request, "delivery/create_delivery_staff.html", {"form": form})
