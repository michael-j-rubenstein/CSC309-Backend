# Generated by Django 4.1.3 on 2022-11-17 22:47

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_users_is_active_remove_users_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='users',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
