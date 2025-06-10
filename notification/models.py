from django.db import models
from user.models import CustomUser

# Create your models here.
class NotificationMessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ManyToManyField(CustomUser, related_name="notification")
    message = models.ForeignKey(NotificationMessage, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    

    def __repr__(self):
        return f"{self.message.message}"