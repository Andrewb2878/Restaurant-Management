from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import MenuItem  # Import your model
from .models import UserProfile 
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def menu(request):
    # Fetch available menu items from the database
    menu_items = MenuItem.objects.filter(available=True)  
    # Pass the data to the template
    return render(request, 'core/menu.html', {'menu_items': menu_items})



def is_chef(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Chef"

@login_required
@user_passes_test(is_chef)
def chef_dashboard(request):
    return render(request, "core/chef_dashboard.html")

def is_waiter(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Waiter"

@login_required
@user_passes_test(is_waiter)
def waiter_dashboard(request):
    return render(request, "core/waiter_dashboard.html")



def portal(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                # Retrieve user profile & role
                user_profile = UserProfile.objects.get(user=user)

                # Redirect based on role
                if user_profile.role == "Chef":
                    return redirect("chef_dashboard")
                elif user_profile.role == "Waiter":
                    return redirect("waiter_dashboard")
                elif user_profile.role == "Manager":
                    return redirect("manager_dashboard")
                else:
                    logout(request)
                    messages.error(request, "Your account does not have an assigned role. Please contact your manager.")
                    return redirect("portal")  # Default fallback

            except UserProfile.DoesNotExist:
                logout(request)
                messages.error(request, "Your account does not have a user profile. Please contact your manager.")
                return redirect("portal")

    else:
        form = AuthenticationForm()

    return render(request, 'core/portal.html', {"form": form})