from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
import json
from .models import MenuItem, UserProfile, Feedback  # Importing  model
from .forms import PortalLoginForm, FeedbackForm
from staff_scheduling.models import Schedule, Shift  # Importing the model from stuff scheduling app


# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def menu(request):
    # Fetch available menu items from the database
    menu_items = MenuItem.objects.filter(available=True)  
    # Pass the data to the template
    return render(request, 'core/menu.html', {'menu_items': menu_items})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('feedback')
        else:
            # Loop through form errors and display each one
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = FeedbackForm()

    return render(request, 'core/feedback.html', {'form': form})


def is_manager(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Manager"


@login_required
@user_passes_test(is_manager)
def view_feedback(request):
    feedback = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'core/view_feedback.html', {'feedback': feedback})


@login_required
@user_passes_test(is_manager)
def toggle_feedback_read(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.read = not feedback.read  # Toggle the read status
        feedback.save()
        return JsonResponse({'success': True, 'read': feedback.read})
    except Feedback.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Feedback not found'})


@login_required
@user_passes_test(is_manager)
def delete_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    return JsonResponse({'success': True})


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
    shifts = Shift.objects.filter(staff=request.user)  # Fetch shifts specific to the logged-in waiter
    
    shifts_dict = {}
    for shift in shifts:
        shift_date = shift.start_time.strftime('%Y-%m-%d')  # Extract date from shift's start time
        shift_info = f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')} | Role: {shift.role}"

        if shift_date in shifts_dict:
            shifts_dict[shift_date].append(shift_info)  # Append multiple shifts per day
        else:
            shifts_dict[shift_date] = [shift_info]

    return render(request, "core/waiter_dashboard.html", {"shifts_json": json.dumps(shifts_dict)})


def portal(request):
    if request.method == 'POST':
        form = PortalLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                user_profile = UserProfile.objects.get(user=user)
                role = user_profile.role

                if role == "Chef":
                    return redirect("chef_dashboard")
                elif role == "Waiter":
                    return redirect("waiter_dashboard")
                elif role == "Manager":
                    return redirect("manager_dashboard")
                else:
                    logout(request)
                    messages.error(request, "Your account does not have an assigned role.")
                    return redirect("portal")
            except UserProfile.DoesNotExist:
                logout(request)
                messages.error(request, "Your account does not have a user profile.")
                return redirect("portal")
    else:
        form = PortalLoginForm()

    return render(request, 'core/portal.html', {"form": form})