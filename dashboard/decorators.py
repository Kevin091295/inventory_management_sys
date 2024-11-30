from django.http import HttpResponse
from django.shortcuts import redirect


def auth_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard-index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


# def allowed_users(allowed_roles=[]):
#     def decorators(view_func):
#         def wrapper(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You are not authorized to view this page')
#         return wrapper
#     return decorators


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