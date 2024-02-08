from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxInput

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm, StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(forms.ModelForm,StyleFormMixin):
    class Meta:
        model = User
        fields = ('is_active',)
        widgets = {
            'is_anything_required': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
        }
