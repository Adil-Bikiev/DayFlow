from django.contrib import admin

from .models import Task, TaskCompletion


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time', 'is_recurring', 'repeat_days_display', 'date', 'is_active')
    list_filter = ('is_recurring', 'is_active', 'user')
    search_fields = ('title', 'description')


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('task', 'date', 'completed')
    list_filter = ('completed', 'date')