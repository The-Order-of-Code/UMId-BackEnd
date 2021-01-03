from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tickets", TicketViewSet, basename="tickets")
router.register("ticketTypes", TicketTypeViewSet, basename="ticketTypes")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("ticketLogs", TicketLogViewSet, basename="ticketLogs")

urlpatterns = [
    path("", include(router.urls)),
    path("validateTicket", validateTicket)
]
