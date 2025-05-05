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
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == "Manager"

@login_required
@user_passes_test(is_manager)  # Restrict access to managers
def manager_dashboard(request):  
    all_shifts = Shift.objects.all()  # Fetch all scheduled shifts
    return render(request, 'staff_scheduling/manager_dashboard.html', {'shifts': all_shifts})

@login_required
@user_passes_test(is_manager)
def manager_schedule(request):
    all_shifts = Shift.objects.all()  
    return render(request, 'staff_scheduling/manager_schedule.html', {'shifts': all_shifts})


@login_required
@user_passes_test(is_manager)
def create_schedule(request):
    staffs = User.objects.filter(userprofile__role__in=["Chef", "Waiter"])  # Query only staff roles

    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)  # Save form but don’t commit yet
            schedule.save()  # Save the main object first
            form.save_m2m()  # Then save ManyToMany relationships (staff)
            return redirect('manager_dashboard')  # Redirect after saving
    else:
        form = ScheduleForm()

    return render(request, 'staff_scheduling/create_schedule.html', {'form': form, 'staffs': staffs})


