from django.urls import path, include
from .views import SubscriptionOne, SubscriptionAll, CreateStripeCheckoutSession, \
    CreateSubscription, UpdateSubscription, SuccessCheckout, DeleteSubscription, \
    GetPrevInvoices, GetUpcomingInvoice, UpdatePaymentMethod, Unsubscribe, UnsuccessfulCheckout, GetUserSubscription

urlpatterns = [
    path('<int:pk>/', SubscriptionOne.as_view(), name='subscriptions_one'),
    path('subscribe/<int:pk>/', CreateStripeCheckoutSession.as_view(),
         name='checkout_session'),
    path('unsubscribe/', Unsubscribe, name='subscription_unsubscribe'),
    path('', SubscriptionAll.as_view(), name='subscriptions_all'),
    path('add/', CreateSubscription, name='subscription_create'),
    path('update/<int:id>/', UpdateSubscription, name='subscription_update'),
    path('delete/<int:id>/', DeleteSubscription, name='sub'),
    path('subscribe/success/<str:session_id>/',
         SuccessCheckout, name='checkout_success'),
    path('subscribe/failed/', UnsuccessfulCheckout, name='checkout_failed'),
    path('invoice/history/', GetPrevInvoices, name='user_prev_invoices'),
    path('invoice/upcoming/', GetUpcomingInvoice, name='user_next_invoice'),
    path('update/payment/', UpdatePaymentMethod, name="update_payment_method"),
    path('me/', GetUserSubscription, name="user_subscription")
]
