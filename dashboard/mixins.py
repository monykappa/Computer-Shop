from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

class SuperuserRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a superuser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            return redirect(reverse_lazy('home:home')) 
        return super().dispatch(request, *args, **kwargs)


# class StaffRequiredMixin(AccessMixin):
#     """
#     Verify that the current user is authenticated and is staff (not necessarily superuser).
#     Allows access to admin views and dashboard but no permission to edit or add.
#     """
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return self.handle_no_permission()

#         # Allow staff members (including superusers) to access
#         if not request.user.is_staff:
#             return self.handle_no_permission()

#         # Optional: Check for specific permissions if needed
#         # if not request.user.has_perm('your_app.can_view_dashboard'):
#         #     return self.handle_no_permission()

#         return super().dispatch(request, *args, **kwargs)

#     def handle_no_permission(self):
#         # Customize redirection here, for example:
#         return redirect(reverse_lazy('home:home'))  