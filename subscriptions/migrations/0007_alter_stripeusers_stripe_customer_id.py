# Generated by Django 4.1.3 on 2022-11-17 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_rename_usersubscriptions_stripeusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripeusers',
            name='stripe_customer_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
