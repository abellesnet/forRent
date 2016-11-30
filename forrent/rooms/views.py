from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from rooms.forms import CreateRoomForm, UpdateRoomForm
from rooms.models import Room


class MyRoomsListView(LoginRequiredMixin, ListView):
    template_name = 'myrooms_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Room.objects.filter(host=self.request.user).order_by('-available_since') \
            .select_related('host').prefetch_related('amenity_set')


class RoomCreateView(PermissionRequiredMixin, CreateView):
    form_class = CreateRoomForm
    template_name = 'room_form.html'
    permission_required = ('rooms.add_room',)

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super(RoomCreateView, self).form_valid(form)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'


class RoomUpdateView(PermissionRequiredMixin, UpdateView):
    model = Room
    form_class = UpdateRoomForm
    template_name = 'room_form.html'

    def has_permission(self):
        room = Room.objects.filter(pk=self.kwargs.get('pk')).first()
        if room and room.host == self.request.user:
            return True
        return False


class RoomDeleteView(PermissionRequiredMixin, DeleteView):
    model = Room
    template_name = 'room_delete.html'
    success_url = reverse_lazy('myrooms_list')

    def has_permission(self):
        room = Room.objects.filter(pk=self.kwargs.get('pk')).first()
        if room and room.host == self.request.user:
            return True
        return False


class RoomListView(ListView):
    template_name = 'room_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Room.objects.filter(available_to__gt=now()).order_by('-available_since') \
            .select_related('host').prefetch_related('amenity_set')
