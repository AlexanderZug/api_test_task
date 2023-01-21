from django.contrib import admin

from .models import Task, User


class TaskInline(admin.TabularInline):
    model = Task
    extra = 3


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)
    inlines = (TaskInline,)
