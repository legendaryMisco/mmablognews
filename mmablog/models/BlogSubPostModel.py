from django.db import models
from mmablog.models.BlogPostModel import BlogPost
from mmablog.models.BlogCategoryModel import BlogCategory
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import uuid
import os


def topic_image_file_path(instance, filename):
    # Construct the file path based on the album's title and the song's title
    return os.path.join('blog/photos', instance.category.name, filename)
    

class BlogSubPost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    blogheadline = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    topic_image  = models.ImageField(upload_to=topic_image_file_path,null=True, blank=True,validators=[
            FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png']),
        ],)
    topic = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    article = models.TextField(null=True,blank=True)
    total_clicks = models.BigIntegerField(default=0)
    total_comments = models.BigIntegerField(default=0)   
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_publisher')
    author = models.ManyToManyField(User, related_name='%(class)s_author') 
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-topic_image']
        db_tablespace = 'BSPtableIndexStorage'
        
        indexes = [models.Index(fields=['topic_image', 'topic', 'article', 'posted_date'])]    
    
    
    def sub_topic_image(self):
        try:
            return self.topic_image.url
        except:
            return ''
    
    
    def __str__(self):
        return self.topic