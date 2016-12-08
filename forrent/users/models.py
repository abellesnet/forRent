from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, DateTimeField
from django.db.models import Model
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField

from users.settings import DEFAULT_PROFILE_PHOTO_OPTIONS

PROFILE_PHOTO_ROOT = 'profile/photo/'


def photo_filename(instance, filename):
    extension = filename.split('.')[-1]
    return '{0}{1}.{2}'.format(PROFILE_PHOTO_ROOT, instance.user.username, extension)


class Profile(Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    photo = ThumbnailerImageField(resize_source=DEFAULT_PROFILE_PHOTO_OPTIONS, upload_to=photo_filename)
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})
