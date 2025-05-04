from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Shift
from .forms import ScheduleForm
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def staff_schedule(request): # View to display the schedule for the logged-in staff member.
    shifts = Shift.objects.filter(staff=request.user)
    return render(request, 'staff_scheduling/staff_schedule.html', {'shifts': shifts})



def is_manager(user):
    return user.is_authenticated and user.userprofile.role == "Manager"

@user_passes_test(is_manager)
def manager_schedule(request): # View to display the schedule for all staff members, accessible only to managers.
    all_shifts = Shift.objects.all()
    return render(request, 'staff_scheduling/manager_schedule.html', {'shifts': all_shifts})

@user_passes_test(is_manager)
def create_schedule(request):  # View to create a new schedule, accessible only to managers.
    staffs = User.objects.all()  # Query all users who can be assigned to a schedule

    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager_schedule')  # Redirect to the manager's view
    else:
        form = ScheduleForm()

    return render(request, 'staff_scheduling/create_schedule.html', {'form': form, 'staffs': staffs})


def test_template(request):
    staffs = User.objects.all()  # Get all registered users
    return render(request, 'staff_scheduling/create_schedule.html', {'staffs': staffs})
