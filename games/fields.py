from django.db.models import ImageField
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class CompressedImageField(ImageField):
    def __init__(self, *args, **kwargs):
        self.max_width = kwargs.pop('max_width', 1200)
        self.max_height = kwargs.pop('max_height', 1200)
        self.quality = kwargs.pop('quality', 80)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        if file and not file._committed:
            # Open the image
            image = Image.open(file)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                image = image.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            width, height = image.size
            if width > self.max_width or height > self.max_height:
                ratio = min(self.max_width / width, self.max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save the compressed image
            output = BytesIO()
            image.save(output, format='JPEG', quality=self.quality, optimize=True)
            output.seek(0)
            
            # Generate a new filename
            name, ext = os.path.splitext(file.name)
            new_filename = f"{name}_compressed.jpg"
            
            # Save the compressed file
            file.save(new_filename, ContentFile(output.read()), save=False)
            
        return file 