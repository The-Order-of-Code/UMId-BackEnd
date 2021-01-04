"""EasyID URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

############ Only to have all paths in main page, idk how else to do it ########################################
from general.views import UserViewSet, CourseViewSet, StudentViewSet, EmployeeViewSet, AllViewSet
from library.views import RoomViewSet, ReservationViewSet
from cafeteria.views import TicketViewSet, TicketTypeViewSet, ProfileViewSet, TicketLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("courses", CourseViewSet, basename="courses")
router.register("students", StudentViewSet, basename="students")
router.register("employees", EmployeeViewSet, basename="employees")
router.register("all", AllViewSet, basename="all")
router.register("rooms", RoomViewSet, basename="rooms")
router.register("reservations", ReservationViewSet, basename="reservations")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("ticketTypes", TicketTypeViewSet, basename="ticketTypes")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("ticketLogs", TicketLogViewSet, basename="ticketLogs")
############ Only to have all paths in main page, idk how else to do it ########################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
    path("general/", include("general.urls")),
    path("library/", include("library.urls")),
    path("cafeteria/", include("cafeteria.urls")),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),  # Returns the default icon(prevents error message)
]

# Used to serve images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
