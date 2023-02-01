from django.views.generic import CreateView
from django.urls import reverse

from .forms import RegisterModelForm

# Create your views here.
class UserRegistrationView(CreateView):
    form_class = RegisterModelForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse("login_user")
