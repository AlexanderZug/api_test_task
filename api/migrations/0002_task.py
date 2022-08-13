# Generated by Django 4.1 on 2022-08-13 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_title", models.CharField(max_length=120)),
                ("task_description", models.TextField()),
                ("task_completion", models.DateField()),
                (
                    "file",
                    models.FileField(
                        blank=True, upload_to="files/", verbose_name="загрузка файла"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]