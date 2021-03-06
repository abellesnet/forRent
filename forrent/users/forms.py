# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm
from django.utils.translation import ugettext_lazy as _

from users.models import Profile


class CreateUserForm(UserCreationForm):
    first_name = CharField(label=_('First name'), max_length=30, min_length=1)
    last_name = CharField(label=_('Last name'), max_length=30, min_length=1)
    email = CharField(min_length=1)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'groups',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_with_same_email = User.objects.filter(email=email)
        if user_with_same_email.count() > 0:
            raise ValidationError(_('A user with that email already exists.'))
        return email

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if len(groups) != 1:
            raise ValidationError(_('You must select one group.'))
        return groups

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit)
        if commit:
            user.groups = self.cleaned_data.get('groups')
            Profile.objects.get_or_create(user=user)
        return user


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        labels = {
            'photo': _('Photo'),
        }
