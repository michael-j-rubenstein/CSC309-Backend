# Generated by Django 4.1.3 on 2022-11-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_users_is_active_users_is_admin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(null=True, upload_to='accounts/images'),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
