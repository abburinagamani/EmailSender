from django.db import models

# Create your models here.
class EmailLog(models.Model):
    to_email = models.TextField()  # allows multiple addresses
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment_names = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)  # e.g. "Sent" or "Failed"
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.to_email} on {self.sent_at.strftime('%Y-%m-%d %H:%M')}"