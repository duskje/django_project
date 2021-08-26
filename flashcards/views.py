from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.views.generic import FormView, TemplateView

from django.urls import reverse_lazy

from . import forms


class UserDecksView(LoginRequiredMixin, TemplateView):
    template_name = 'user_decks.html'


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('decks')

    def form_valid(self, form):
        user = get_user_model()

        user.objects.create_user(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
            email=form.cleaned_data.get('email'),
        )

        return super().form_valid(form)


