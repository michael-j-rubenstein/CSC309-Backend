from django.urls import path, include
from .views import SubscriptionOne, SubscriptionAll, CreateStripeCheckoutSession, \
    CreateSubscription, UpdateSubscription, SuccessCheckout, DeleteSubscription

urlpatterns = [
    path('<int:pk>/', SubscriptionOne.as_view(), name='subscriptions_one'),
    path('checkout/<int:pk>/', CreateStripeCheckoutSession.as_view(),
         name='checkout_session'),
    path('', SubscriptionAll.as_view(), name='subscriptions_all'),
    path('add/', CreateSubscription, name='subscription_create'),
    path('update/<int:id>/', UpdateSubscription, name='subscription_update'),
    path('delete/<int:id>/', DeleteSubscription, name='sub'),
    path('checkout/success/<str:session_id>/',
         SuccessCheckout, name='checkout_success')
]
