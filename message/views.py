from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from message.models import Message
from message.serializers import MessageSerializer, CreateMessageSerializer
from django.db.models import Q

# Create your views here.
class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMessageSerializer
        return MessageSerializer

    def get_queryset(self):   # get message url => /message/?receiver=1
        if self.request.user.is_staff:
            return Message.objects.select_related("sender").select_related("receiver").all()
        else:
            receiver_id = self.request.query_params.get("receiver")
            return Message.objects.select_related("sender").select_related("receiver").filter(Q(sender=self.request.user, receiver_id=receiver_id) | Q(sender=receiver_id, receiver_id=self.request.user))