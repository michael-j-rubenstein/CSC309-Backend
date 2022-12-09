from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from .models import Subscription, StripeUser, StripeUserLog

from django.conf import settings
import json
import stripe

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):

    model = Subscription
    list_display = ['name', 'amount', 'type']
    # exclude = ['price_id']
    readonly_fields = ('price_id', 'id')

    def clean(self):
        name = self.cleaned_data.get('name')
        amount = self.cleaned_data.get('amount')
        type = self.cleaned_data.get('type')

        if name == '' or amount == '' or type == '':
            raise ValueError("Fields cannot be left blank")

        return self.cleaned_data

    def save_model(self, request, obj, form, change):

        data = form.cleaned_data
        name = data.get('name', '')
        amount = data.get('amount', '')
        type = data.get('type', '')

        stripe.api_key = settings.STRIPE_SECRET_KEY

        print(form.changed_data, obj.id)

        if 'change' in request.path:

            subscription = obj
            try:
                print("here now")

                stripe.Product.modify(
                    str(obj.id),
                    name=name
                )
                print("here now")

                stripe.Price.modify(str(subscription.price_id),
                                    active=False)

                new_price_id = stripe.Price.create(
                    nickname=name,
                    product=str(subscription.id),
                    currency="cad",
                    unit_amount=int(amount * 100),
                    recurring={"interval": "month" if type == 'M' else 'year'},
                )

                subscription.price_id = new_price_id.id

                super().save_model(request, obj, form, change)

            except Exception as e:
                print(e)
                return

        else:
            try:
                obj.save()
                stripe.Product.create(name=name, id=str(obj.id))
                price_id = stripe.Price.create(
                    nickname=name,
                    product=str(obj.id),
                    currency="cad",
                    unit_amount=int(amount * 100),
                    recurring={"interval": "month" if type == 'M' else 'year'},
                )

                obj.price_id = price_id.id

                super().save_model(request, obj, form, change)

            except Exception as e:
                print(e)
                return

    def delete_model(self, request, obj):
        print(obj)
        try:
            all_subscriptions = stripe.Subscription.list()

            wanted_subscriptions = []

            stripe_customer = StripeUser.objects.all().filter(subscription=obj.id)

            stripe_customer_ids = {
                customer.stripe_customer_id for customer in stripe_customer}

            if len(stripe_customer) != 0:
                for subscription in all_subscriptions:

                    if subscription.customer in stripe_customer_ids:
                        wanted_subscriptions.append(subscription)

            for subscription in wanted_subscriptions:
                stripe.Subscription.delete(subscription.id)

            stripe.Product.modify(str(obj.id), active=False)

            for customer in stripe_customer:
                customer.delete()

            stripe.Price.modify(
                obj.price_id, active=False)

            obj.delete()

        except Exception as e:
            print(e)
            return

    def delete_queryset(self, request, queryset):
        print(queryset)

        try:
            for obj in queryset:
                all_subscriptions = stripe.Subscription.list()

                wanted_subscriptions = []

                stripe_customer = StripeUser.objects.all().filter(subscription=obj.id)

                stripe_customer_ids = {
                    customer.stripe_customer_id for customer in stripe_customer}

                if len(stripe_customer) != 0:
                    for subscription in all_subscriptions:

                        if subscription.customer in stripe_customer_ids:
                            wanted_subscriptions.append(subscription)

                for subscription in wanted_subscriptions:
                    stripe.Subscription.delete(subscription.id)

                stripe.Product.modify(str(obj.id), active=False)

                for customer in stripe_customer:
                    customer.delete()

                stripe.Price.modify(
                    obj.price_id, active=False)

            queryset.delete()

        except Exception as e:
            print(e)
            return


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(StripeUser)
admin.site.register(StripeUserLog)
