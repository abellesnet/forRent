from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from forrent.settings import HOSTS_GROUP_NAME
from rooms.forms import CreateRoomForm


class CreateRoomView(PermissionRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'room_create.html'
    success_url = '/'

    def has_permission(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        return HOSTS_GROUP_NAME in self.request.user.groups.values_list('name', flat=True)

    def form_valid(self, form):
        room = form.save(commit=False)
        room.host = self.request.user
        return super(CreateRoomView, self).form_valid(form)
