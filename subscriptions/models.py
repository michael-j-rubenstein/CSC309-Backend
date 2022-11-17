from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from accounts.models import User
from django.contrib.auth.models import User

# Create your models here.


class Subscription(models.Model):
    MONTH = 'M'
    YEAR = 'Y'
    TYPES = [(MONTH, 'Monthly'), (YEAR, 'Yearly')]

    name = models.CharField(max_length=50, null=False, unique=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], null=False)
    price_id = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=7, choices=TYPES, default=MONTH)

    def __str__(self):
        return str(self.name) + " ($" + str(self.amount) + "/ " + str(self.type) + ")"


# TODO: Need to have another table that maps users to subscriptions or can have it in user table

class StripeUsers(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(
        max_length=200, null=False, unique=True)
