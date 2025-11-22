from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """
    Model to store uploaded CSV datasets with summary information.
    """
    filename = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    summary_json = models.JSONField()
    csv_path = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-upload_timestamp']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_timestamp}"
