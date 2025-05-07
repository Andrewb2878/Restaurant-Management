from django import forms
from .models import Schedule
from django.utils import timezone
from django.contrib.auth.models import User

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'start_date', 'end_date', 'staff']  
        staff = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(userprofile__role__in=["Chef", "Waiter"]),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}))



        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Schedule Name',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'staff': 'Select Staff Members',
        }



        