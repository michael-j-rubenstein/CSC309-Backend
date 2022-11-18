from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Subscription, StripeUser, StripeUserLog
from .serializers import SubscriptionSerializer

from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

import stripe
import json
from django.conf import settings

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionOne(RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Subscription.objects.all()


class SubscriptionAll(ListAPIView):
    serializer_class = SubscriptionSerializer
    model = Subscription
    queryset = Subscription.objects.all()


class CreateStripeCheckoutSession(APIView):

    def post(self, request, *args, **kwargs):
        user_has_subscription = len(
            StripeUser.objects.all().filter(user_id=request.user.id)) == 1

        if user_has_subscription:
            return JsonResponse({"error": "User already has a subscription"})

        subscription_id = self.kwargs['pk']
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=1,
                line_items=[
                    {
                        'price': subscription.price_id,
                        # 'price_data': {
                        #     'currency': 'cad',
                        #     'unit_amount': int(subscription.amount * 100),
                        #     'product_data': {
                        #         'name': subscription.name
                        #     }
                        # },
                        'quantity': 1
                    }
                ],
                mode='subscription',
                metadata={
                    'user_id': 1,
                    'product_id': subscription.id
                },
                success_url='http://127.0.0.1:8000/subscriptions/checkout/success/{CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/subscriptions/checkout?success=false'
            )
            # return redirect(checkout_session.url)
            return JsonResponse({'sessionUrl': checkout_session.url})
        except Exception as e:
            return JsonResponse({'msg': 'Something went wrong!', 'error': str(e)}, status=500)


@api_view(["GET"])
def SuccessCheckout(request, session_id):
    if request.method == 'GET':
        session = stripe.checkout.Session.retrieve(session_id)

        customer = stripe.Customer.retrieve(session.customer)

        customer_id = customer.id
        user_id = request.user
        subscription_id = session.metadata.product_id

        print(request.user)

        new_user = StripeUser(user_id=user_id,
                              stripe_customer_id=customer_id, subscription_id=subscription_id)
        new_user_log = StripeUserLog(
            user=user_id, stripe_customer_id=customer_id)
        new_user.save()
        new_user_log.save()
        # invoices = stripe.Invoice.list(customer=customer_id).data
        # for invoice in invoices:
        #     invoice_data = {
        #         "invoice_id": invoice.id,
        #         "invoice_total": invoice.total,
        #         "amount_paid": invoice.amount_paid,
        #         "customer": invoice.customer,
        #         "invoice_link": invoice.hosted_invoice_url,
        #         "invoice_period": invoice.lines.data[0].period
        #     }
        #     print(invoice_data)
        # for subscription in subscription_list:
        #     print("-------------------------------")
        return JsonResponse({"success": session_id})


@api_view(["POST"])
def CreateSubscription(request):

    if not request.user.is_superuser:
        return JsonResponse({"error": "User does not have permission to add a new subscription"})

    if request.method == 'POST':

        payload = json.loads(request.body)
        name = payload.get('name', '')
        amount = payload.get('amount', '')
        type = payload.get('type', '')

        if name == '' or amount == '' or type == '':
            raise ValidationError

        if len(Subscription.objects.all().filter(name=name)) != 0:
            return JsonResponse({"error": "Plan name already exists, please choose a different name"})

        if type not in {"M", "Y"}:
            return JsonResponse({"error": """Incorrect type, please choose M for monthly or Y for yearly"""})

        if amount < 0:
            return JsonResponse({"error": "Amount field cannot be negative"})

        subscription = Subscription(name=name, amount=amount, type=type)
        subscription.save()
        subscription_id = subscription.id
        stripe.Product.create(name=name, id=subscription_id)
        price_id = stripe.Price.create(
            nickname=name,
            product=str(subscription_id),
            currency="cad",
            unit_amount=int(float(amount) * 100),
            recurring={"interval": "month" if type == 'M' else 'year'},
        )
        subscription.price_id = price_id.id
        subscription.save()
        return JsonResponse({
            "id": subscription_id,
            "name": name,
            "amount": amount,
            "type": "Monthly" if type == 'M' else "Yearly"
        })


@api_view(["POST"])
def UpdateSubscription(request, id):
    if request.method == 'POST':

        subscription = get_object_or_404(Subscription, id=id)

        payload = json.loads(request.body)

        name = payload.get('name', '')
        amount = payload.get('amount', '')
        type = payload.get('type', '')

        if name != '' and isinstance(name, str):
            subscription.name = name
            stripe.Product.modify(
                str(subscription.id),
                name=name
            )

        if amount != '' and isinstance(amount, float):
            subscription.amount = amount
            print('asdad', amount, isinstance(
                amount, float), subscription.price_id)
            stripe.Price.modify(str(subscription.price_id),
                                active=False)
            print('asdad', amount, isinstance(amount, float))
            new_price_id = stripe.Price.create(
                nickname=name,
                product=str(subscription.id),
                currency="cad",
                unit_amount=int(amount * 100),
                recurring={"interval": "month" if type == 'M' else 'year'},
            )
            subscription.price_id = new_price_id.id
            print(subscription.price_id)

        # if type != '' and type in {'M', 'Y'}:
        #     subscription.type = type
        #     stripe.Price.modify(subscription.price_id,
        #                         recurring={"interval": "month" if type == 'M' else 'year'})

        subscription.save()

        return JsonResponse({"success": subscription.id})


@api_view(["POST"])
def DeleteSubscription(request, id):
    if request.method == "POST":
        subscription_exists = len(
            Subscription.objects.all().filter(id=id)) != 0
        if not subscription_exists:
            return JsonResponse({"error": "Subscription Doesn't Exist"})

        all_subscriptions = stripe.Subscription.list()

        wanted_subscriptions = []

        stripe_customer = StripeUser.objects.all().filter(subscription=id)

        if len(stripe_customer) != 0:
            for subscription in all_subscriptions:
                if subscription.customer == stripe_customer.stripe_customer_id:
                    wanted_subscriptions.append(subscription)

        for subscription in wanted_subscriptions:
            stripe.Subscription.delete(subscription.id)

        stripe.Product.modify(str(id), active=False)

        for customer in stripe_customer:
            customer.delete()

        local_subscription = Subscription.objects.all().filter(id=id)[0]

        stripe.Price.modify(
            local_subscription.price_id, active=False)

        local_subscription.delete()

        return JsonResponse({"success": "Subscription deleted successfully!"})


@api_view(["GET"])
def GetPrevInvoices(request):
    if request.user.is_authenticated:
        print("asdad")

    user_logs = StripeUserLog.objects.all().filter(id=request.user.id)

    stripe_customer_ids = []

    for log in user_logs:
        stripe_customer_ids.append(log.stripe_customer_id)

    print(stripe_customer_ids)

    all_invoices = []

    for customer_id in stripe_customer_ids:
        invoices = stripe.Invoice.list(customer=customer_id).data
        for invoice in invoices:
            print(invoice)
            invoice_data = {
                "invoice_id": invoice.id,
                "invoice_total": invoice.total,
                "amount_paid": invoice.amount_paid,
                "customer": invoice.customer,
                "invoice_link": invoice.hosted_invoice_url,
                "invoice_period": invoice.lines.data[0].period,
                "plan": {
                    "active": invoice.lines.data[0].plan.active,
                    "name": invoice.lines.data[0].plan.nickname,
                    "type": invoice.lines.data[0].plan.interval
                }
            }
            all_invoices.append(invoice_data)
    return JsonResponse({"invoices": all_invoices})
