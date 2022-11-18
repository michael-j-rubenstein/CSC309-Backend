from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from .models import Subscription, StripeUser

from django.conf import settings
import json
import stripe

# Register your models here.


# class SubscriptionAdmin(admin.ModelAdmin):

#     list_display = ['name', 'amount', 'type']

#     def save_model(self, request, obj, form, change):

#         data = form.cleaned_data
#         name = data.get('name', '')
#         amount = data.get('amount', '')
#         type = data.get('type', '')

#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         if 'change' in request.path:
#             temp = request.path[34:]
#             id = int(temp[:temp.index('/')])
#             # TODO: update stripe product
#         else:
#             product_id = stripe.Product.create(name=name).id
#             # print(product_id)
#         super().save_model(request, obj, form, change)


# admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Subscription)
admin.site.register(StripeUser)
