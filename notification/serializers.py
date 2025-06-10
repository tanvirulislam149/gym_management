from rest_framework import serializers
from notification.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "receiver", "message", "is_global", "is_read"]
        read_only_fields = ["is_global", "is_read"]