from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views.generic import CreateView, FormView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from rooms.forms import CreateRoomForm, UpdateRoomForm, RoomSearchForm
from rooms.models import Room, RoomBooking


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
        qs = Room.objects.filter(available_to__gt=now()).order_by('-available_since') \
            .select_related('host').prefetch_related('amenity_set')
        if self.request.GET.get('location_search'):
            qs = qs.filter(address__icontains=self.request.GET.get('location_search'))
        if self.request.GET.get('accommodates_min'):
            qs = qs.filter(accommodates__gte=self.request.GET.get('accommodates_min'))
        if self.request.GET.get('accommodates_max'):
            qs = qs.filter(accommodates__lte=self.request.GET.get('accommodates_max'))
        if self.request.GET.get('price_min'):
            qs = qs.filter(price_per_day__gte=self.request.GET.get('price_min'))
        if self.request.GET.get('price_max'):
            qs = qs.filter(price_per_day__lte=self.request.GET.get('price_max'))
        return qs


class RoomSearchView(FormView):
    template_name = 'room_search.html'
    form_class = RoomSearchForm

    def get_success_url(self):
        url = reverse('room_list')
        qs = '&'.join(
            ['='.join((field, value,)) for field, value in self.request.POST.items() if field != 'csrfmiddlewaretoken']
        )
        return '?'.join((url, qs))


class RoomBookingListView(LoginRequiredMixin, ListView):
    template_name = 'roombooking_list.html'
    paginate_by = 12

    def get_queryset(self):
        return RoomBooking.objects.filter(guest=self.request.user).order_by('-since').select_related('room', 'guest', )


class RoomBookingDeleteView(PermissionRequiredMixin, DeleteView):
    model = RoomBooking
    template_name = 'roombooking_delete.html'
    success_url = reverse_lazy('roombooking_list')

    def has_permission(self):
        roombooking = RoomBooking.objects.filter(pk=self.kwargs.get('pk')).first()
        if roombooking and roombooking.guest == self.request.user:
            return True
        return False
