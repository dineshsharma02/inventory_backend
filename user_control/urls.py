

from django.urls import path,include
from .views import CreateUserView,LoginUserView,UpdatePaasswordView,MeView,UserActivityView,UsersView

from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash = False)

router.register("create-user",CreateUserView,"create user")
router.register("login",LoginUserView,"login")
router.register("update-password",UpdatePaasswordView,"update password")
router.register("me",MeView,"me")
router.register("activities-log",UserActivityView,"activities log")
router.register("users",UsersView,"users")

urlpatterns = [
    path("", include(router.urls)),
]
