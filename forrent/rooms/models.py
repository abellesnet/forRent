import glob
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import ForeignKey, CharField, TextField, BooleanField, DecimalField, DateField, IntegerField, \
    DateTimeField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.urls import reverse
from django.utils.crypto import get_random_string
from easy_thumbnails.fields import ThumbnailerImageField

from rooms.lib import generate_responsive_room_main_photo_images
from rooms.settings import DEFAULT_IMAGE_OPTIONS


class RoomAmenity(Model):
    name = CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "room amenities"

    def __str__(self):
        return self.name


ROOM_IMAGE_ROOT = 'post/image/'


def random_filename(instance, filename):
    extension = filename.split('.')[-1]
    return '{0}{1}.{2}'.format(ROOM_IMAGE_ROOT, get_random_string(16), extension)


def remove_photos(filename):
    pattern = '{}{}'.format(os.path.join(settings.MEDIA_ROOT, filename), '*')
    for file in glob.glob(pattern):
        os.remove(file)


class Room(Model):
    host = ForeignKey(User)
    name = CharField(max_length=128)
    description = TextField(null=True, blank=True)
    accommodates = IntegerField(validators=[MinValueValidator(1)])
    beds = IntegerField(validators=[MinValueValidator(1)])
    private_bathroom = BooleanField()
    amenity_set = ManyToManyField(RoomAmenity, blank=True)
    price_per_day = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    available_since = DateField()
    available_to = DateField()
    main_photo = ThumbnailerImageField(resize_source=DEFAULT_IMAGE_OPTIONS, upload_to=random_filename)
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('host', 'name',)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.host.get_full_name())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self.pk is None
        response = super(Room, self).save(force_insert, force_update, using, update_fields)
        if is_new:
            generate_responsive_room_main_photo_images(self.main_photo)
        return response

    def delete(self, using=None, keep_parents=False):
        remove_photos(self.main_photo.name)
        return super(Room, self).delete(using, keep_parents)

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'pk': self.pk})

    def get_main_photo_extension(self):
        if not self.main_photo:
            return None
        name, extension = os.path.splitext(self.main_photo.name)
        return extension

    def image_extension(self):
        if not self.main_photo:
            return None
        name, extension = os.path.splitext(self.main_photo.name)
        return extension
