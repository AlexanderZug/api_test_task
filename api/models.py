from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(
        verbose_name='Полное имя пользователя', max_length=30
    )

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='task')
    task_title = models.CharField(max_length=120)
    task_description = models.TextField()
    task_completion = models.DateField()
    file = models.FileField(
        verbose_name='загрузка файла',
        upload_to='files/',
        blank=True,
    )

    def __str__(self):
        return self.task_title
