from django.db import models
from datetime import date

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    @property
    def computed_status(self):
        if self.status == "Completed":
            return "Completed"
        return "Overdue" if self.due_date < date.today() else "Pending"