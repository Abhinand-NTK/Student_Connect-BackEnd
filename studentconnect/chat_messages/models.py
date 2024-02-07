from django.db import models

from superadmin.models import UserAccount

# Create your models here.

class Message(models.Model):
    """
    Models for  the message
    """
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"From: {self.sender.first_name} To: {self.receiver.first_name}"