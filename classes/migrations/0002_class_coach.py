# Generated by Django 4.1.3 on 2022-11-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="class",
            name="coach",
            field=models.CharField(default="admin", max_length=50),
        ),
    ]