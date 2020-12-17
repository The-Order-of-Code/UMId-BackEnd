from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tickets", TicketViewSet, basename="tickets")
router.register("ticketTypes", TicketTypeViewSet, basename="ticketTypes")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
]
