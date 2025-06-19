from rest_framework.serializers import ModelSerializer
from message.models import Message
from user.models import CustomUser

class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]

class MessageSerializer(ModelSerializer):
    sender = SimpleUserSerializer()
    receiver = SimpleUserSerializer()
    
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message_text", "is_read"]
        read_only_fields = ["is_read"]


class CreateMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message_text", "is_read"]
        read_only_fields = ["is_read"]