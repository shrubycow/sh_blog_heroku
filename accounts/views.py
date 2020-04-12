from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django_registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from .forms import AvatarForm

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
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            if str(cur_profile.avatar) != 'no-avatar-300x300.jpg':
                cur_profile.avatar.delete()
            cur_profile.avatar = form.cleaned_data['avatar']
            cur_profile.save()
            return redirect('accounts:profile')
    else:
        form = AvatarForm()
    return render(request, 'registration/profile.html', {'cur_profile': cur_profile, 'form': form})


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