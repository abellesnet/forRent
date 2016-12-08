from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from forrent.settings import LOGIN_URL
from users.forms import CreateUserForm, UpdateProfileForm
from users.models import Profile


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'user_create.html'
    success_url = LOGIN_URL


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'


class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'profile_form.html'

    def has_permission(self):
        profile = Profile.objects.filter(pk=self.kwargs.get('pk')).first()
        if profile and profile.user == self.request.user:
            return True
        return False
