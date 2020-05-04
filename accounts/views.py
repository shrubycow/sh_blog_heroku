from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django_registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from sh_blog.models import UserProfile
import os

from sh_blog.models import UserProfile
# Create your views here.
class MyRegistrationView(RegistrationView):
    form_class = RegistrationFormUniqueEmail
    disallowed_url = reverse_lazy("accounts:django_registraion_disallowed")
    success_url = reverse_lazy("accounts:django_registration_complete")            


class MyActivationView(ActivationView):
    success_url = reverse_lazy("accounts:django_registration_activation_complete")

    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        self.new_profile(user)
        return user


    def new_profile(self, user):
        new_profile = UserProfile()
        new_profile.user = user
        new_profile.save()

@login_required
def profile(request):
    cur_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'registration/profile.html', {'cur_profile': cur_profile})


class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    subject_template_name = 'registration/email_subject.txt'
    email_template_name = 'registration/email_template.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done1.html'
    title = ('Пароль успешно сброшен')
    

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm1.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class MyPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete1.html'
    title = ('Пароль успешно сброшен')

def avatars_change(request):
    base_dir = os.getcwd()
    avatar_dir = os.path.join(base_dir, 'static', 'accounts', 'avatars')
    files_list = []
    for root, dirs, files in os.walk(avatar_dir):
        files_list = files

    return render(request, 'avatars.html', {'avatars': files_list})

def avatar_to_profile(request, avatar_str):
    cur_user = UserProfile.objects.get(user=request.user)
    cur_user.avatar = avatar_str
    cur_user.save()

    return redirect('accounts:profile')