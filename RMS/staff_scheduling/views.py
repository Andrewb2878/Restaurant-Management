from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from reservation.models import Reservation
from .models import Schedule, Shift
from .forms import ScheduleForm
from datetime import date, timedelta


import json  # json for serialization

@login_required
def staff_schedule(request):
    # Fetch shifts for the logged-in staff member
    shifts = Shift.objects.filter(staff=request.user)

    # Prepare shifts data for the calendar
    shifts_dict = {}
    for shift in shifts:
        shift_date = shift.start_time.strftime('%Y-%m-%d')
        shift_info = f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')} | Role: {shift.role}"

        if shift_date in shifts_dict:
            shifts_dict[shift_date].append(shift_info)
        else:
            shifts_dict[shift_date] = [shift_info]

    # Serialize shifts_dict to JSON
    shifts_json = json.dumps(shifts_dict)

    # Determine the dashboard URL based on the user's role
    if request.user.groups.filter(name="Manager").exists():
        dashboard_url = "manager_dashboard"
    elif request.user.groups.filter(name="Waiter").exists():
        dashboard_url = "waiter_dashboard"
    elif request.user.groups.filter(name="Chef").exists():
        dashboard_url = "chef_dashboard"
    else:
        dashboard_url = "portal"  # Default fallback

    return render(request, "staff_scheduling/staff_schedule.html", {
        "shifts_json": shifts_json,  # Pass serialized JSON to the template
        "dashboard_url": dashboard_url,
    })
def is_manager(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Manager"

@login_required
@user_passes_test(is_manager)  # Restrict access to managers
def manager_dashboard(request):  
    today = date.today()

    # Reservation data to display on dashboard
    reservation_count = Reservation.objects.count()
    recent_reservations = Reservation.objects.order_by('-created_at')[:5]

    shifts = Schedule.objects.all()
    response = render(request, 'staff_scheduling/manager_dashboard.html', {
        'shifts': shifts,
        'reservation_count': reservation_count,
        'recent_reservations': recent_reservations,
    })

    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

@login_required
@user_passes_test(is_manager)
def manager_schedule(request):
    all_shifts = Shift.objects.all()  
    return render(request, 'staff_scheduling/manager_schedule.html', {'shifts': all_shifts})


@login_required
@user_passes_test(is_manager)
def create_schedule(request):
    staffs = User.objects.filter(userprofile__role__in=["Chef", "Waiter","Manager"])  # Query only staff roles
    form = ScheduleForm()  # Initialize the form outside the conditional to ensure availability
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    if request.method == "POST":
        form = ScheduleForm(request.POST)  # No duplicate request check
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            form.save_m2m()
            print("Schedule saved in DB:", Schedule.objects.all())  # Debugging statement
            return redirect('manager_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)

    return render(request, 'staff_scheduling/create_schedule.html', {
        'form': form,
        'staffs': staffs,
        'tomorrow': tomorrow
    })

@login_required
@user_passes_test(is_manager)
def view_schedules(request):  
    schedules = Schedule.objects.all()  # Fetch all schedules
    shifts = Shift.objects.all() # Fetch all shifts
    return render(request, 'staff_scheduling/view_schedules.html', {'schedules': schedules, 'shifts': shifts})
