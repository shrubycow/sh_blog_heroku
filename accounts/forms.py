from django import forms
from sh_blog.models import UserProfile
from django.core import validators

class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='Сменить аватар',
    validators=[validators.FileExtensionValidator(allowed_extensions=('gif', 'jpg', 'png'))],
    error_messages={'invalid_extension': 'Этот формат не поддерживается'})
    
    class Meta:
        model = UserProfile
        fields = ['avatar']