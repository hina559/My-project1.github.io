from django.db import models
from django.conf import settings
from django.utils import timezone

def case_image_path(instance, filename):
    """Generate unique image path for case images"""
    import uuid
    # Get file extension
    ext = filename.split('.')[-1]
    # Create unique filename with case info and timestamp
    unique_filename = f"case_{instance.farmer.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    return f'cases/{instance.farmer.id}/{timezone.now().strftime("%Y%m%d")}/{unique_filename}'

class Analysis(models.Model):
    """Plant disease analysis results"""
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses')
    image = models.ImageField(upload_to=case_image_path, blank=True, null=True)
    crop_name = models.CharField(max_length=100)
    disease_name = models.CharField(max_length=100)
    analysis_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-analysis_date']

    def __str__(self):
        return f"{self.farmer.username} - {self.crop_name} - {self.disease_name}"


class Case(models.Model):
    """Cases opened by farmers"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_cases'
    )


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Case #{self.id} - {self.farmer.username} - {self.status}"


class CaseMessage(models.Model):
    """Two-way chat messages for cases"""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in Case #{self.case.id}"
