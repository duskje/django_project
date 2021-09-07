from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django import forms


class FlashcardReviewForm(forms.Form):
    flashcard_ids = forms.HiddenInput()


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username:')
    email = forms.EmailField(label='Email:')

    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            },
        )
    )

    password_confirm = forms.CharField(
        label='Type your password again:',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password",
            },
        )
    )

    def clean_username(self):
        user: User = get_user_model()
        username = self.cleaned_data.get('username')
        matching_username = user.objects.filter(username__exact=username)

        if matching_username.exists():
            raise forms.ValidationError('Username or email already taken')

        return username

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
