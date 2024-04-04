from django.db import models
from mmablog.models.BlogPostModel import BlogPost
import uuid
import os


class BlogViewCount(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    blogheadline = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    ip_information = models.JSONField(null=True,blank=True)
    viewed_date = models.DateTimeField(auto_now_add=True)
    
    
    
    

    