from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("rooms", RoomViewSet, basename="rooms")
router.register("reservations", ReservationViewSet, basename="reservations")

urlpatterns = [
    path("", include(router.urls)),
]
