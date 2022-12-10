# Generated by Django 4.1.3 on 2022-12-08 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0013_remove_classes_end_date_remove_classes_end_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="classes",
            name="end_date",
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="classes",
            name="end_time",
            field=models.TimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="classes",
            name="start_time",
            field=models.TimeField(default=None, null=True),
        ),
    ]