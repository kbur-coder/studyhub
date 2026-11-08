from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

PROJECT_IMAGE_SIZE = (600, 400)
AVATAR_SIZE = (200, 200)


def shrink_into(field, uploaded, max_size, quality):
    if uploaded is None:
        return
    image = Image.open(uploaded)
    if image.size[0] <= max_size[0] and image.size[1] <= max_size[1]:
        uploaded.seek(0)
        return
    image_format = image.format or 'JPEG'
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffer = BytesIO()
    image.save(buffer, format=image_format, quality=quality)
    field.save(uploaded.name, ContentFile(buffer.getvalue()), save=False)
