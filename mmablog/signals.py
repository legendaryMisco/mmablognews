import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from mmablog.models.BlogPostModel import BlogPost

@receiver(post_save, sender=BlogPost)
def resize_image(sender, instance, created, **kwargs):
    if created:  # Only resize if a new instance is created
        # Open the original image
        with Image.open(instance.topic_image.path) as image:
                # Resize the image
                
            image = image.convert('RGB')
            new_size = (110, 110)
            resized_image = image.resize(new_size)
            # Save the resized image to the new image field
            img_byte_array = BytesIO()
            resized_image.save(img_byte_array, format='JPEG')
            img_byte_array.seek(0)
            
            
            instance.topic_image_small.save(
                os.path.basename(instance.topic_image.name),
                ContentFile(img_byte_array.getvalue()),
                save=True
            )