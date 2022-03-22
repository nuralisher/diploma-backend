import uuid
from io import BytesIO
from PIL import Image, ImageDraw

import qrcode
from django.core.files import File
from django.db import models
import qrcode.image.svg

class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        factory = qrcode.image.svg.SvgPathImage
        qrcode_img = qrcode.make(self.id, box_size=24, border=1,  image_factory=factory)
        buffer = BytesIO()
        qrcode_img.save(stream=buffer)
        fname = f'qr_code-{self.id}' + '.svg'
        self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)
