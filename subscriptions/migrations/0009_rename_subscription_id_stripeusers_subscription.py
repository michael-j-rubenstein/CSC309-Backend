# Generated by Django 4.1.3 on 2022-11-18 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0008_stripeusers_subscription_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripeusers',
            old_name='subscription_id',
            new_name='subscription',
        ),
    ]
