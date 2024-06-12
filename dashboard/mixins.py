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