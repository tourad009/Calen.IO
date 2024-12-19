from django.db import models
from user_app.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True, verbose_name='Date de début')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin')
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        default='medium'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    def clean(self):
        if self.due_date and self.end_date and self.due_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")