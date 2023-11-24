from django.urls import path
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from config import settings

from users.views import RegisterView, ProfileView, ChangePassword, verify_email_sent, verify_email


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('profile/verify_email_sent', verify_email_sent, name='verify_email_sent'),
    path('profile/verify_email/<str:token>',
         verify_email, name='verify_email_link'),

    path('profile/change_password',
         ChangePassword.as_view(), name='change_password'),

    path('reset_password/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             email_template_name="users/password_reset_email.html",
             subject_template_name="users/password_reset_subject.txt",
             from_email=settings.EMAIL_HOST_USER),
         name='reset_password'),
    path('reset_password_sent/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
