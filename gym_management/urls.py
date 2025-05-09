"""
URL configuration for gym_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from plans.views import PlansViewSet, FitnessClassesViewSet, ScheduledClassViewSet
from bookings.views import BookPlansViewSet, BookClassesViewSet, AttendenceViewSet, PaymentPlansViewSet
from bookings.views import initiate_payment, payment_cancel, payment_success, payment_fail
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings


router = DefaultRouter()
router.register("plans", PlansViewSet, basename="plans")
router.register("fitness_classes", FitnessClassesViewSet, basename="fitness_classes")
router.register("scheduled_classes", ScheduledClassViewSet, basename="scheduled_classes")
router.register("book_plans", BookPlansViewSet, basename="book_plans")
router.register("book_classes", BookClassesViewSet, basename="book_classes")
router.register("attendence", AttendenceViewSet, basename="attendence")
router.register("payment", PaymentPlansViewSet, basename="payment")





schema_view = get_schema_view(
   openapi.Info(
      title="MuscleGain - Gym management API",
      default_version='v1',
      description="API documentation for gym management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tanvirulislam149@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path("makePayment/initiate/", initiate_payment, name="initiate-payment"),
    path("makePayment/success/", payment_success, name="payment-success"),
    path("makePayment/fail/", payment_fail, name="payment-fail"),
    path("makePayment/cancel/", payment_cancel, name="payment-cancel"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
