from django.db import models

# Create your models here.
class Reminder(models.Model):
    REMINDER_METHOD_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    ]
    reminder_datetime = models.DateTimeField()
    message = models.TextField()
    reminder_method = models.CharField(max_length=10, choices=REMINDER_METHOD_CHOICES, default='EMAIL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reminder for {self.reminder_datetime.strftime('%Y-%m-%d %H:%M')} via {self.reminder_method}"