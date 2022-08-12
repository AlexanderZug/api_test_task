# Generated by Django 4.1 on 2022-08-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "api",
            "0008_remove_task_user_task_user_task_alter_taskuser_task_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="user_task",
        ),
        migrations.AddField(
            model_name="task",
            name="user_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
