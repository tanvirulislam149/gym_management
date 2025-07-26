from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from message.models import Message
from message.serializers import MessageSerializer, CreateMessageSerializer

# Create your views here.
class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMessageSerializer
        return MessageSerializer

    def get_queryset(self):
        receiver_id = self.request.query_params.get("receiver")
        return Message.objects.filter(sender=self.request.user, receiver_id=receiver_id)