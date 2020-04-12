from django.urls import path
from .views import MyRegistrationView, MyActivationView, profile, MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, MyPasswordResetComplete
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('accounts/profile/', profile, name="profile"),
    path('accounts/password_reset/', MyPasswordResetView.as_view(), name="reset"),
    path('accounts/password_reset_done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', MyPasswordResetComplete.as_view(), name='password_reset_complete'),
    path(
       "accounts/activate/complete/",
       TemplateView.as_view(
           template_name="django_registration/activation_complete.html"
       ),
       name="django_registration_activation_complete",
    ),
    path(
        "accounts/activate/<str:activation_key>/",
        MyActivationView.as_view(),
        name="django_registration_activate",
    ),
    path(
        "accounts/register/",
        MyRegistrationView.as_view(),
        name="django_registration_register",
    ),
    path(
        "accounts/register/complete/",
        TemplateView.as_view(
            template_name="django_registration/registration_complete.html"
        ),
        name="django_registration_complete",
    ),
    path(
        "accounts/register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html"
        ),
        name="django_registration_disallowed",
    ),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]