from django.urls import path, include
from rest_framework_nested import routers
from notification.views import NotificationViewSet

router = routers.DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notifications")


urlpatterns = [
    path('', include(router.urls)),
]