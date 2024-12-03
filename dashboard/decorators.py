from django.http import HttpResponse
from django.shortcuts import redirect


def auth_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard-index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is a superuser, if yes, allow access
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if the user is in one of the allowed groups
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page", status=403)
        
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """
    Allow only superusers to access the view.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to view this page.", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_or_admin(view_func):
    """
    Allow both superusers and staff users to access the view.
    """
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return HttpResponse("You are not authorized to view this page.", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
