from django.urls import path, include
from .views import TicketViewSet, TicketWalletViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tickets", TicketViewSet, basename="tickets")
router.register("ticketsWallet", TicketWalletViewSet, basename="ticketsWallet")

urlpatterns = [
    path("", include(router.urls)),
]
