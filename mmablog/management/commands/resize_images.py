import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from mmablog.models.BlogPostModel import BlogPost

class Command(BaseCommand):
    help = 'Resizes existing images and saves them to the new image field'

    def handle(self, *args, **kwargs):
        images = BlogPost.objects.all()
        for instance in images:
            # Open the original image
            with Image.open(instance.topic_image.path) as image:
                # Resize the image
                
                image = image.convert('RGB')
                new_size = (364, 273)
                resized_image = image.resize(new_size)
                # Save the resized image to the new image field
                img_byte_array = BytesIO()
                resized_image.save(img_byte_array, format='JPEG')
                img_byte_array.seek(0)
                
                
                instance.topic_image.save(
                    os.path.basename(instance.topic_image.name),
                    ContentFile(img_byte_array.getvalue()),
                    save=True
                )
