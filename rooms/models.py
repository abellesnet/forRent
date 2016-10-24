from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import ForeignKey, CharField, TextField, BooleanField, DecimalField, DateField, IntegerField, \
    DateTimeField
from django.db.models import ImageField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.urls import reverse


class RoomAmenity(Model):
    name = CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "room amenities"

    def __str__(self):
        return self.name


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
    main_photo = ImageField()
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('host', 'name',)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.host.get_full_name())

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'pk': self.pk})
