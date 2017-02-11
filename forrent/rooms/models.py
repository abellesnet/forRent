import glob
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import ForeignKey, CharField, TextField, BooleanField, DecimalField, DateField, IntegerField, \
    DateTimeField, Avg
from django.db.models import ManyToManyField
from django.db.models import Model
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from easy_thumbnails.fields import ThumbnailerImageField

from rooms.lib import generate_responsive_room_main_photo_images
from rooms.settings import DEFAULT_IMAGE_OPTIONS


class RoomAmenity(Model):
    name = CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "room amenities"

    def __str__(self):
        return self.name


ROOM_IMAGE_ROOT = 'room/image/'


def random_filename(instance, filename):
    extension = filename.split('.')[-1]
    return '{0}{1}.{2}'.format(ROOM_IMAGE_ROOT, get_random_string(16), extension)


def remove_photos(filename):
    pattern = '{}{}'.format(os.path.join(settings.MEDIA_ROOT, filename), '*')
    for file in glob.glob(pattern):
        os.remove(file)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


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

    def get_start_date(self):
        return max(self.available_since, now().date())

    def get_end_date(self):
        return self.available_to

    def get_dates_unavailable(self):
        # dates_unavailable = '["2017-03-15","2017-03-16"]'
        bookings = RoomBooking.objects.filter(room=self, to__gte=self.get_start_date())
        dates_unavailable = []
        for booking in bookings:
            for single_date in daterange(booking.since, booking.to):
                dates_unavailable.append('"{0}"'.format(single_date.isoformat()))
        return '[{0}]'.format(','.join(dates_unavailable))

    def get_past_guests(self):
        past_bookings = self.roombooking_set.filter(to__lt=now())
        return User.objects.filter(roombooking__in=past_bookings)

    def rating(self):
        return self.roomrating_set.aggregate(Avg('rate')).get('rate__avg')


class RoomBooking(Model):
    room = ForeignKey(Room)
    guest = ForeignKey(User)
    since = DateField()
    to = DateField()
    total_price = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.room)


class RoomRating(Model):
    room = ForeignKey(Room)
    guest = ForeignKey(User)
    rate = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('room', 'guest',)

    def __str__(self):
        return str(self.room)


class RoomComment(Model):
    room = ForeignKey(Room)
    author = ForeignKey(User)
    comment = TextField()
    created_at = DateTimeField(auto_now_add=True)
