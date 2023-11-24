from pprint import pprint
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import UserProfileForm, UserRegisterForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from users.models import User
from users.services import send_verification_code



class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self) -> str:

        url = reverse('verify_email_link', args=[
            self.object.email_verification_token])
        full_url = self.request.build_absolute_uri(url)
        print(self.object.email)
        print(full_url)
        send_verification_code(self.object.email, full_url)

        return reverse_lazy('verify_email_sent')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email_sent(request):
    return render(request, 'users/verify_email_sent.html')


def verify_email(request, token):
    user = User.objects.get(email_verification_token=token)
    user.is_active = True
    user.save()
    # Redirect to a success page or login page
    return render(request, 'users/email_verified.html')


class ChangePassword(PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'users/change_password.html'

    def get_success_url(self) -> str:
        logout(self.request)
        return reverse('login')
