from django import forms
from .models import Schedule
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and start_date <= date.today():
            self.add_error('start_date', "Start date must be from tomorrow onwards.")

        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', "End date must be after the start date.")

        return cleaned_data