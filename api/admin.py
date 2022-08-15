from django.contrib import admin

from .models import Task, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'name',
    )
    search_fields = ('name',)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'task_title',
        'task_description',
        'task_completion',
        'file',
    )
    search_fields = ('task_title',)
    list_filter = ('task_completion',)


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
