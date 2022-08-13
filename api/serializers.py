import datetime as dt

from rest_framework import serializers

from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            'id',
            'user',
            'task_title',
            'task_description',
            'task_completion',
            'file',
        )

    def validate_task_completion(self, value):
        today = dt.date.today()
        if value < today:
            raise serializers.ValidationError(
                'Проверьте время завершения задачи!'
            )
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'task',
        )
