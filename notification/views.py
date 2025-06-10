from django.shortcuts import render
from rest_framework import viewsets
from notification.models import Notification
from notification.serializers import NotificationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]
