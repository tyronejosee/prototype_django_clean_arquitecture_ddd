import io

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def generate_test_image_file() -> SimpleUploadedFile:
    """Generate a temporary image in memory for use in tests."""
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), "blue")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("example.jpg", file.read(), content_type="image/jpeg")
