from django.urls import path

from rest_framework import routers

from payment.views import PaymentViewSet, PaymentSuccessView, PaymentCancelView

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("<int:pk>/success/",
         PaymentSuccessView.as_view(),
         name="payment-success"),
    path("<int:pk>/cancel/",
         PaymentCancelView.as_view(),
         name="payment-cancel"),
] + router.urls

app_name = "payment"

