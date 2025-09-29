from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser

# ----------------------------------------
# Event Model
# ----------------------------------------
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.date}"


# ----------------------------------------
# Notification Model
# ----------------------------------------
class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="The user who will receive this notification"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.recipient.username}] {self.title}"


