from django.db import models

# Create your models here.
class Tasks(models.Model):
    """
    Fields match the assignment specification:
    - title (string)
    - due_date (date)
    - estimated_hours (decimal)
    - importance (integer, 1-10 scale)
    - dependencies (list of task IDs)
    - completed (boolean) - added for tracking
    """
    
    title = models.TextField(
        max_length=200,
        help_text='Task title/description'
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text='When is the task due? (YYYY-MM-DD)'
    )
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Estimated hours to complete the task, e.g., 2.5 hours'
    )
    importance = models.IntegerField(
        default=5,
        help_text='Rate the task importance out of 10'
    )
    dependencies = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="Comma-separated list of task IDs this task depends on (e.g., '1,3,5')"
    )
    completed = models.BooleanField(
        default=False,
        help_text="Has this task been completed?"
    )
    def __str__(self):
        return f"Task {self.id}: {self.title}"