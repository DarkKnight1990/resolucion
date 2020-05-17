from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic.edit import FormView

from accounts.forms import (
    OrganizationForm, UserLoginForm
)


class OrganizationCreateView(FormView):
    form_class = OrganizationForm
    template_name = 'accounts/create_org.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def home(request):
    print(request.user.is_authenticated)
    return render(request, 'home.html')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_field_name = 'home'
    authentication_form = UserLoginForm
