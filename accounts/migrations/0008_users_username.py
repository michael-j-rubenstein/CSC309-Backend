# Generated by Django 4.1.3 on 2022-11-17 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_users_is_active_alter_users_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
