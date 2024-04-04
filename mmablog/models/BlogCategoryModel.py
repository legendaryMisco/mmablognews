from django.db import models
import uuid

class BlogCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    name = models.CharField(max_length=200)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_tablespace = 'BCtableIndexStorage'
        
        indexes = [models.Index(fields=['name'])]    
    
    def __str__(self):
        return self.name