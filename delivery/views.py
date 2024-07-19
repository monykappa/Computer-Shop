from shared_imports import *


@login_required
def dashboard(request):
    try:
        delivery_staff = request.user.deliverystaff
    except DeliveryStaff.DoesNotExist:
        return render(request, 'delivery/not_delivery_staff.html')

    # Total completed deliveries
    total_completed = DeliveryAssignmentHistory.objects.filter(delivery_staff=delivery_staff).count()

    # Pending deliveries
    pending_deliveries = DeliveryAssignment.objects.filter(
        delivery_staff=delivery_staff,
        completed_at__isnull=True
    ).select_related('order')

    # Completed deliveries (last 7 days)
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    completed_deliveries = DeliveryAssignmentHistory.objects.filter(
        delivery_staff=delivery_staff,
        completed_at__gte=seven_days_ago
    ).select_related('order')

    # Daily completed deliveries (last 7 days)
    daily_completed = DeliveryAssignmentHistory.objects.filter(
        delivery_staff=delivery_staff,
        completed_at__gte=seven_days_ago
    ).values('completed_at__date').annotate(count=Count('id')).order_by('completed_at__date')

    context = {
        'delivery_staff': delivery_staff,
        'total_completed': total_completed,
        'pending_deliveries': pending_deliveries,
        'completed_deliveries': completed_deliveries,
        'daily_completed': daily_completed,
    }

    return render(request, 'delivery/dashboard.html', context)


class DeliveryGuyDashboardView(LoginRequiredMixin, ListView):
    template_name = "delivery/delivery_order.html"
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


