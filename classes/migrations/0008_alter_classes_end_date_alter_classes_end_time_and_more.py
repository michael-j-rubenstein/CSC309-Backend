# Generated by Django 4.1.3 on 2022-12-08 22:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0007_alter_classes_end_date_alter_classes_end_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classes",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(2022, 12, 8, 17, 59, 20, 73181)
            ),
        ),
        migrations.AlterField(
            model_name="classes",
            name="end_time",
            field=models.TimeField(default=datetime.time(17, 59, 20, 73181)),
        ),
        migrations.AlterField(
            model_name="classes",
            name="start_time",
            field=models.TimeField(default=datetime.time(17, 59, 20, 73181)),
        ),
    ]
