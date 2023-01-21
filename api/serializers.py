import datetime as dt

from rest_framework import serializers

from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = '__all__'

    def validate_task_completion(self, value):
        """
        Метод проверяет, что пользователь не
        поставил время завершения задачи в прошлом.
        """
        today = dt.date.today()
        if value < today:
            raise serializers.ValidationError(
                'Проверьте время завершения задачи!'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
