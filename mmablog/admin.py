from django.contrib import admin
from .models import BlogCategory,BlogComment, BlogContact, BlogPost, BlogSubPost,BlogViewCount

class BlogCatgoryDisplayTable(admin.ModelAdmin):
    list_display = ['name', 'added_date', 'updated_date']
    
    
class BlogPostDisplayTable(admin.ModelAdmin):
    list_display = ['topic', 'topic_image', 'category', 'publisher', 'posted_date', 'updated_date']
    
class BloGSubPostDisplayTable(admin.ModelAdmin):
    list_display = ['topic', 'topic_image', 'category', 'publisher', 'posted_date', 'updated_date']

    
class BlogViewCountDisplayTable(admin.ModelAdmin):
    list_display = ['blogheadline', 'viewed_date']
    
class BlogPostCommentDisplayTable(admin.ModelAdmin):
    list_display = ['blogheadline', 'message', 'comment_date']





admin.site.register(BlogSubPost, BloGSubPostDisplayTable)
admin.site.register(BlogCategory, BlogCatgoryDisplayTable)
admin.site.register(BlogComment,BlogPostCommentDisplayTable)
admin.site.register(BlogContact)
admin.site.register(BlogViewCount, BlogViewCountDisplayTable)
admin.site.register(BlogPost, BlogPostDisplayTable)