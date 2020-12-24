from django.core.exceptions import ValidationError
from django.conf import settings
from decimal import *


def readable_size(size_in):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size_in >= 1024:
        i += 1
        size_in = size_in / 1024
    return f'{Decimal(str(round(size_in,1))).normalize()}{sizes[i]}'


def validate_image_size(obj):
    filesize = obj.file.size
    limit = settings.PROFILE_PICTURE_UPLOAD_MAX_SIZE
    print(readable_size(1024))
    if filesize > limit:
        raise ValidationError(f'This file size is {readable_size(filesize)}, max size is {readable_size(limit)}')
