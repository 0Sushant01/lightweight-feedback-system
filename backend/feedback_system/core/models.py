from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user with role
class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='team')

    def __str__(self):
        return f"{self.username} ({self.role})"

# Feedback model
class Feedback(models.Model):
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    )

    employee = models.ForeignKey(User, related_name='received_feedback', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='given_feedback', on_delete=models.CASCADE)
    strengths = models.TextField()
    areas_to_improve = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    acknowledged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.manager.username} → {self.employee.username} [{self.sentiment}]"
