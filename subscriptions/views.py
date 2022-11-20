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
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()


class SubscriptionAll(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    model = Subscription
    queryset = Subscription.objects.all()


class CreateStripeCheckoutSession(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_has_subscription = len(
            StripeUser.objects.all().filter(user_id=request.user.id)) == 1

        if user_has_subscription:
            return JsonResponse({"error": "User already has a subscription"})

        subscription_id = self.kwargs['pk']
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                line_items=[
                    {
                        'price': subscription.price_id,
                        'quantity': 1
                    }
                ],
                mode='subscription',
                metadata={
                    'user_id': request.user.id,
                    'product_id': subscription.id
                },
                success_url='http://127.0.0.1:8000/subscriptions/subscribe/success/{CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/subscriptions/subscribe?success=false'
            )

            return JsonResponse({'sessionUrl': checkout_session.url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def SuccessCheckout(request, session_id):
    if request.method == 'GET' and request.user.is_authenticated:

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

        try:

            stripe.Product.create(name=name, id=subscription_id)
            price_id = stripe.Price.create(
                nickname=name,
                product=str(subscription_id),
                currency="cad",
                unit_amount=int(amount * 100),
                recurring={"interval": "month" if type == 'M' else 'year'},
            )
            subscription.price_id = price_id.id
            subscription.save()

        except Exception as e:
            return JsonResponse({"error": str(e)})

        return JsonResponse({
            "id": subscription_id,
            "name": name,
            "amount": amount,
            "type": "Monthly" if type == 'M' else "Yearly"
        })


@api_view(["POST"])
def UpdateSubscription(request, id):

    if not request.user.is_superuser:
        return JsonResponse({"error": "User does not have permission to update a subscription"})

    if request.method == 'POST':

        subscription = get_object_or_404(Subscription, id=id)

        payload = json.loads(request.body)

        name = payload.get('name', '')
        amount = payload.get('amount', '')
        type = payload.get('type', '')

        errors = []

        if name == '':
            errors.append("name field is required")
        if amount == '':
            errors.append("amount field is required")
        if type == '':
            errors.append("type field is required")

        if len(errors) > 0:
            return JsonResponse({"error": errors})

        try:

            if isinstance(name, str):
                subscription.name = name
                stripe.Product.modify(
                    str(subscription.id),
                    name=name
                )
            else:
                return JsonResponse({"error": "name must be a string"})

            if isinstance(amount, float) and type in {'M', 'Y'}:
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

            else:
                return JsonResponse({"error": "type or amount invalid, type: M for monthly, Y for yearly, amount: float number e.g. 19.99"})

            subscription.save()

        except Exception as e:

            return JsonResponse({"error": str(e)})

        return JsonResponse({"success": subscription.id})


@ api_view(["POST"])
def DeleteSubscription(request, id):

    if not request.user.is_superuser:
        return JsonResponse({"error": "User does not have permission to delete a subscription"})

    if request.method == "POST":
        subscription_exists = len(
            Subscription.objects.all().filter(id=id)) != 0
        if not subscription_exists:
            return JsonResponse({"error": "Subscription Doesn't Exist"})

        try:

            all_subscriptions = stripe.Subscription.list()

            wanted_subscriptions = []

            stripe_customer = StripeUser.objects.all().filter(subscription=id)

            stripe_customer_ids = {
                customer.stripe_customer_id for customer in stripe_customer}

            if len(stripe_customer) != 0:
                for subscription in all_subscriptions:
                    print(subscription.customer)
                    if subscription.customer in stripe_customer_ids:
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

        except Exception as e:

            return JsonResponse({"error": str(e)})

        return JsonResponse({"success": "Subscription deleted successfully!"})


@ api_view(["GET"])
def GetPrevInvoices(request):

    if request.method == 'GET' and request.user.is_authenticated:
        print("asdad")

    user_logs = StripeUserLog.objects.all().filter(user_id=request.user.id)

    stripe_customer_ids = []

    for log in user_logs:
        stripe_customer_ids.append(log.stripe_customer_id)

    print(stripe_customer_ids)

    all_invoices = []

    try:

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

    except Exception as e:

        return JsonResponse({"error": str(e)})

    return JsonResponse({"invoices": all_invoices})


@ api_view(["GET"])
def GetUpcomingInvoice(request):
    if request.method == 'GET' and request.user.is_authenticated:

        stripe_users = StripeUser.objects.all().filter(user_id=request.user.id)

        if len(stripe_users) == 0:
            return JsonResponse({"error": "User does not have an active subscription"})

        customer_id = stripe_users[0].stripe_customer_id

        invoice = stripe.Invoice.upcoming(customer=customer_id)

        invoice_data = {
            "invoice_id": None,
            "invoice_total": invoice.total,
            "amount_paid": invoice.amount_paid,
            "customer": invoice.customer,
            "invoice_link": None,
            "invoice_period": invoice.lines.data[0].period,
            "plan": {
                "active": invoice.lines.data[0].plan.active,
                "name": invoice.lines.data[0].plan.nickname,
                "type": invoice.lines.data[0].plan.interval
            }
        }

        return JsonResponse(invoice_data)


@ api_view(["POST"])
def UpdatePaymentMethod(request):
    if request.method == 'POST' and request.user.is_authenticated:

        payload = json.loads(request.body)
        number = payload.get('number', '')
        exp_month = payload.get('exp_month', '')
        exp_year = payload.get('exp_year', '')
        cvc = payload.get('cvc', '')

        if number == '' or exp_month == '' or exp_year == '' or cvc == '':
            raise ValidationError

        try:
            stripe_users = StripeUser.objects.all().filter(user_id=request.user.id)

            if len(stripe_users) == 0:
                return JsonResponse({"error": "User does not have an active subscription"})

            customer_id = stripe_users[0].stripe_customer_id

            all_subscriptions = stripe.Subscription.list()

            subscription_id = ""

            for subscription in all_subscriptions:
                if subscription.customer == customer_id:
                    subscription_id = subscription.id
                    break

            new_payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": str(cvc)
                }
            )

            stripe.PaymentMethod.attach(
                new_payment_method.id, customer=customer_id)

            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    "default_payment_method": new_payment_method.id
                }
            )

            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=new_payment_method.id
            )
        except Exception as e:
            return JsonResponse({"error": str(e)})

        return JsonResponse({"success": "Card has been updated!"})


@ api_view(["POST"])
def Unsubscribe(request):
    if request.method == "POST" and request.user.is_authenticated:

        stripe_users = StripeUser.objects.all().filter(user_id=request.user.id)

        if len(stripe_users) == 0:
            return JsonResponse({"error": "User does not have an active subscription"})

        customer_id = stripe_users[0].stripe_customer_id

        try:
            all_subscriptions = stripe.Subscription.list()

            subscription_id = ""

            for subscription in all_subscriptions:
                if subscription.customer == customer_id:
                    subscription_id = subscription.id
                    break

            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )

            stripe_customer = StripeUser.objects.all().filter(
                user_id=request.user.id)[0]

            subscription_id = stripe_customer.subscription_id

            stripe_customer.delete()

        except Exception as e:
            return JsonResponse({"error": str(e)})

        return JsonResponse({"success": "Unsubscribed from subscription " + str(subscription_id) + " successfully"})
