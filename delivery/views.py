from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from orders.models import OrderStatus
from .forms import *
from userprofile.models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Prefetch



class DeliveryGuyDashboardView(LoginRequiredMixin, ListView):
    template_name = "delivery/dashboard.html"
    context_object_name = "assignments"
    login_url = "dashboard:sign_in"

    def get_queryset(self):
        return (
            DeliveryAssignment.objects.filter(
                delivery_staff__user=self.request.user,
                order__status=OrderStatus.PENDING
            )
            .select_related("order", "order__user")
            .prefetch_related("order__user__address_set")
        )



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

class DeliveryHistoryReportView(LoginRequiredMixin, ListView):
    model = DeliveryAssignmentHistory
    template_name = 'delivery/delivery_history_report.html'
    context_object_name = 'delivery_histories'

    def get_queryset(self):
        try:
            delivery_staff = DeliveryStaff.objects.get(user=self.request.user)
            return DeliveryAssignmentHistory.objects.filter(delivery_staff=delivery_staff).select_related('order')
        except DeliveryStaff.DoesNotExist:
            return DeliveryAssignmentHistory.objects.none()


