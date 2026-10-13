from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


MAX_IMAGE_SIZE = 5 * 1024 * 1024
SUPPORTED_IMAGE_FORMATS = {'JPEG', 'PNG', 'GIF'}


def validate_image_upload(uploaded_file):
    if getattr(uploaded_file, '_committed', False):
        return

    if uploaded_file.size > MAX_IMAGE_SIZE:
        raise ValidationError('Image files must be 5 MB or smaller.')

    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as image:
            image_format = image.format
            image.verify()
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        raise ValidationError('Upload a valid JPG, PNG, or GIF image.') from exc
    finally:
        uploaded_file.seek(0)

    if image_format not in SUPPORTED_IMAGE_FORMATS:
        raise ValidationError('Upload a valid JPG, PNG, or GIF image.')
