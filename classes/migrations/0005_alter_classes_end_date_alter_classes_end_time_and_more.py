# Generated by Django 4.1.3 on 2022-12-08 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0004_classes_end_date_classes_end_time_classes_start_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classes",
            name="end_date",
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="classes",
            name="end_time",
            field=models.TimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="classes",
            name="start_time",
            field=models.TimeField(default=None, null=True),
        ),
    ]
