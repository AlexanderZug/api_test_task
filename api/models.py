from __future__ import annotations

from typing import Union

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager


class User(models.Model):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=30,
    )
    password = models.CharField(max_length=255)
    task: Union[Manager, Task]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task',
        verbose_name='Никнейм',
    )
    task_title = models.CharField(
        verbose_name='Название задачи',
        max_length=120,
    )
    task_description = models.TextField(
        verbose_name='Описание задачи',
    )
    task_completion = models.DateField(
        verbose_name='Дата завершения задачи',
    )
    file = models.FileField(
        verbose_name='Загрузка файла',
        upload_to='files/',
        blank=True,
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self):
        return self.task_title
