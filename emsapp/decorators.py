from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Decorator for SalesAgent
def salesagent_required(view_func):
    """
    Decorator to restrict access to users with 'is_staff' flag.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect unauthenticated users to login page
        if not request.user.is_staff:
            return HttpResponseForbidden("Access Denied: You must be a SalesAgent to view this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


# Decorator for Superuser
def superuser_required(view_func):
    """
    Decorator to restrict access to superusers.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect unauthenticated users to login page
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied: Superuser privileges required.")
        return view_func(request, *args, **kwargs)
    return wrapper
