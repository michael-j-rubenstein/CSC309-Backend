# Generated by Django 4.1.3 on 2022-11-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_users_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
