from django.views.generic import CreateView

from users.forms import CreateUserForm


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'user_create.html'
    success_url = '/'
