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
    ).select_related('order').order_by('-completed_at')

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
        queryset = super().get_queryset()
        
        # Get the delivery staff
        try:
            delivery_staff = DeliveryStaff.objects.get(user=self.request.user)
            queryset = queryset.filter(delivery_staff=delivery_staff)
        except DeliveryStaff.DoesNotExist:
            return DeliveryAssignmentHistory.objects.none()

        # Search by Order ID
        order_id = self.request.GET.get('order_id')
        if order_id:
            queryset = queryset.filter(order__id=order_id)
        
        # Date filtering
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            start_date = parse_datetime(start_date)
            if start_date:
                queryset = queryset.filter(assigned_at__gte=start_date)
        if end_date:
            end_date = parse_datetime(end_date)
            if end_date:
                # Adjust end_date to the last second of the day (23:59:59)
                end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                queryset = queryset.filter(assigned_at__lte=end_date)
        
        # Sorting
        sort_by = self.request.GET.get('sort_by', 'new')  # Default to 'new' for latest data on top
        if sort_by == 'new':
            queryset = queryset.order_by('-assigned_at')
        elif sort_by == 'old':
            queryset = queryset.order_by('assigned_at')
        else:
            # Default sorting (latest first) if 'sort_by' is not 'new' or 'old'
            queryset = queryset.order_by('-assigned_at')
        
        return queryset
