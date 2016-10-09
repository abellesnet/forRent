from django.views.generic import CreateView

from forrent.settings import LOGIN_URL
from users.forms import CreateUserForm


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'user_create.html'
    success_url = LOGIN_URL
