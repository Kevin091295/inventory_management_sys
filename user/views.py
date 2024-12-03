from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Use Django's built-in UserCreationForm
        if form.is_valid():
            user = form.save(commit=False)  # Save the user instance but don't commit yet
            user.is_staff = True  # Mark the user as a staff member
            user.save()  # Save the updated user instance
            
            # Add a success message
            messages.success(request, 'Staff user registered successfully. You can now log in.')

            return redirect('user-login')  # Redirect to login page after registration
        else:
            # Add an error message for invalid submissions
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
    else:
        form = UserCreationForm()  # Instantiate an empty form for GET requests

    context = {
        'form': form  # Pass the form to the template
    }
    return render(request, 'user/register.html', context)  # Render the registration page


def profile(request):
    context = {

    }
    return render(request, 'user/profile.html', context)


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile_update.html', context)
