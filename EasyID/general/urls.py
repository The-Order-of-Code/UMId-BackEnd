from django.urls import path, include
from .views import UserViewSet, CourseViewSet, StudentViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("courses", CourseViewSet, basename="courses")
router.register("students", StudentViewSet, basename="students")
router.register("employees", EmployeeViewSet, basename="employees")

urlpatterns = [
    path("", include(router.urls)),
]
