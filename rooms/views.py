from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import ListView

from rooms.forms import CreateRoomForm
from rooms.models import Room


class MyRoomsListView(LoginRequiredMixin, ListView):
    template_name = 'myrooms_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Room.objects.filter(host=self.request.user).order_by('-available_since').select_related('host')


class RoomCreateView(PermissionRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'room_create.html'
    success_url = '/'
    permission_required = ('rooms.add_room',)

    def form_valid(self, form):
        room = form.save(commit=False)
        room.host = self.request.user
        return super(RoomCreateView, self).form_valid(form)
