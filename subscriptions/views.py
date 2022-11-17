from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import Subscription, StripeUsers
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


# @api_view(['POST'])
# def CreateStripeCheckoutSession(request, pk):
#     if request.method == 'POST':
#         try:
#             subscription = Subscription.objects.get(id=pk)
#             checkout_session = stripe.checkout.Session.create(
#                 client_reference_id=request.user.id if request.user.is_authenticated else None,
#                 line_items=[
#                     {
#                         'price': subscription.price_id,
#                         # 'price_data': {
#                         #     'currency': 'cad',
#                         #     'unit_amount': int(subscription.amount * 100),
#                         #     'product_data': {
#                         #         'name': subscription.name
#                         #     }
#                         # },
#                         'quantity': 1
#                     }
#                 ],
#                 mode='subscription',
#                 metadata={
#                     'user_id': request.user.id if request.user.is_authenticated else None,
#                     'product_id': subscription.id
#                 },
#                 success_url='http://127.0.0.1:8000/subscriptions/checkout/success/{CHECKOUT_SESSION_ID}',
#                 cancel_url='http://127.0.0.1:8000/subscriptions/checkout?success=false'
#             )
#             # return redirect(checkout_session.url)
#             return JsonResponse({'sessionUrl': checkout_session.url})
#         except Exception as e:
#             return JsonResponse({'msg': 'Something went wrong!', 'error': str(e)}, status=500)


class CreateStripeCheckoutSession(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(StripeUsers.objects.all().filter(user_id=request.user))

        subscription_id = self.kwargs['pk']
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
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
                    'user_id': request.user.id if request.user.is_authenticated else None,
                    'product_id': subscription.id
                },
                success_url='http://127.0.0.1:8000/subscriptions/checkout/success/{CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/subscriptions/checkout?success=false'
            )
            # return redirect(checkout_session.url)
            return JsonResponse({'sessionUrl': checkout_session.url})
        except Exception as e:
            return JsonResponse({'msg': 'Something went wrong!', 'error': str(e)}, status=500)


def SuccessCheckout(request, session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)
    customer_id = customer.id
    user_id = request.user
    new_user = StripeUsers(user_id=user_id,
                           stripe_customer_id=customer_id)
    new_user.save()
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


def CreateSubscription(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        name = payload.get('name', '')
        amount = payload.get('amount', '')
        type = payload.get('type', '')

        if name == '' or amount == '' or type == '':
            raise ValidationError

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
