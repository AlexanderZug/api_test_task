from rest_framework import serializers

from .models import Task, TaskUser, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'user_id',
            'task_title',
            'task_description',
            'task_completion',
            'file',
        )


class UserSerializer(serializers.ModelSerializer):
    tasks_for_user = TaskSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'password',
            'tasks_for_user',
            'is_active',
        )

    def create(self, validated_data):
        if 'tasks_for_user' not in self.initial_data:
            user = User.objects.create(**validated_data)
            return user
        tasks_for_user = validated_data.pop('tasks_for_user')
        user = User.objects.create(**validated_data)
        for user_task in tasks_for_user:
            current_user_task, status = Task.objects.get_or_create(**user_task)
            TaskUser.objects.create(task=current_user_task, performer=user)
        return user
