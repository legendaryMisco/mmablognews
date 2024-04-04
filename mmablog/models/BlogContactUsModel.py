from django.db import models
import uuid

class BlogContact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, null=True, blank=True) 
    subject = models.CharField(max_length=280,null=True, blank=True)
    message = models.CharField(max_length=400)
    contacted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    ip_information = models.JSONField(null=True,blank=True)