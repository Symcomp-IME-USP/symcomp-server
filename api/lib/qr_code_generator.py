import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
import os
from django.conf import settings

def generate_qr_code(data: str, size: int = 10) -> tuple[str, ContentFile]:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    
    filename = f'qr_codes/{uuid.uuid4()}.png'
    
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qr_codes'), exist_ok=True)
    
    image_file = ContentFile(buffer.getvalue())
    
    return filename, image_file
