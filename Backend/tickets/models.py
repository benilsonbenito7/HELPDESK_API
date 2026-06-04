from django.db import models
from django.utils import timezone
from django.db import transaction

class Ticket(models.Model):
    
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        CLOSED = 'closed', 'Closed'
        
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
    
    custom_id = models.CharField(max_length=25, unique=True, db_index=True, editable=False, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):    
        if self.pk is None:
            with transaction.atomic():
                super().save(*args, **kwargs)

                self.custom_id = f"TICKET-{timezone.now().year}-{self.pk:05d}"
                super().save(update_fields=["custom_id"])
        else:
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']    
    
    def __str__ (self):
        return f"{self.title} - {self.status}"AA