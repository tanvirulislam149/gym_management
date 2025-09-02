from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from message.models import Message
from user.models import CustomUser

class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name"]

class MessageSerializer(ModelSerializer):
    sender = SimpleUserSerializer()
    receiver = SimpleUserSerializer()
    
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message_text", "is_read", "created_at"]
        read_only_fields = ["is_read"]


class CreateMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message_text", "is_read"]
        read_only_fields = ["is_read", "sender"]

    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(sender=user, **validated_data)
    

class ConversationSerializer(ModelSerializer):
    has_unread = serializers.SerializerMethodField(method_name="get_has_unread")
    # user = SimpleUserSerializer()
    image = serializers.SerializerMethodField(method_name="get_image_url")

    class Meta:
        model = CustomUser
        fields = ["id", "email","first_name", "last_name", "image", "has_unread"]
        read_only_fields = ["has_unread"]

    def get_has_unread(self, obj):
        # return obj.email
        return True if Message.objects.filter(sender = obj, is_read=False).exists() else False
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None