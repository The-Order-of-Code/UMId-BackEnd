from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("rooms", RoomViewSet, basename="rooms")
router.register("freeRooms", FreeRoomViewSet, basename="freeRooms")
router.register("reservations", ReservationViewSet, basename="reservations")
router.register("freeTimes", FreeTimeViewSet, basename="freeTimes")

urlpatterns = [
    path("", include(router.urls)),
]
