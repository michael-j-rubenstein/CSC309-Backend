# Generated by Django 4.1.3 on 2022-11-18 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_alter_stripeusers_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeusers',
            name='subscription_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscription'),
            preserve_default=False,
        ),
    ]
