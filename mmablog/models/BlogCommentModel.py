from django.db import models
from mmablog.models.BlogPostModel import BlogPost
import uuid

class BlogComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    blogheadline = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, null=True, blank=True) 
    website = models.URLField(null=True, blank=True)
    message = models.CharField(max_length=400)
    comment_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    ip_information = models.JSONField(null=True,blank=True)
    
    class Meta:
        db_tablespace = 'BCMtableIndexStorage'
        
        indexes = [models.Index(fields=['name', 'message', 'comment_date'])]    
    def __str__(self):
        return self.message