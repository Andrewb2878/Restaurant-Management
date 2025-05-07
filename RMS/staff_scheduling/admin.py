from django.contrib import admin
from .models import Shift, Schedule


admin.site.register(Shift)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
