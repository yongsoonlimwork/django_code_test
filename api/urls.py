from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("customer-request", views.CustomerRequestModelViewSet, basename="customer_request")

urlpatterns = [
    path('', include(router.urls))
]
