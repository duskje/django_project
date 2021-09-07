import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.timezone import datetime

from django.views.generic import FormView, TemplateView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from . import forms
from .models import Deck, Flashcard


def flashcards_review_view(request, pk):
    template = 'flashcards_review.html'
    context = {
        'pk': pk
    }

    if request.method == 'GET':
        deck = Deck.objects.get(pk=pk)
        flashcards = list(deck.flashcards.all())
        random.shuffle(flashcards)

        try:
            context['current_card'] = flashcards.pop()
        except IndexError:
            raise ValueError('No cards')

        flashcard_ids = [flashcard.id for flashcard in flashcards]
        # context['flashcard_ids'] = flashcard_ids
        form = forms.FlashcardReviewForm
        context['form'] = form
        form.flashcard_ids = flashcard_ids

    elif request.method == 'POST':
        form = forms.FlashcardReviewForm(request.POST)

        try:
            current_card_id = form.flashcard_ids.pop()
        except IndexError:
            return redirect(reverse_lazy('deck-detail', kwargs={'pk': pk}))

        context['current_card'] = Flashcard.objects.get(id=current_card_id)
        context['form'] = form

    else:
        raise ValueError('invalid request')

    return render(request, template, context)


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_deck_deletion.html'

    @property
    def deck_id(self):
        return self.kwargs['pk']

    def get_object(self, queryset=None):
        return Deck.objects.get(pk=self.deck_id)

    def get_success_url(self):
        return reverse_lazy('decks')


class DeckUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['title']
    template_name = 'deck_update.html'

    @property
    def deck_id(self):
        return self.kwargs['pk']

    def get_object(self, queryset=None):
        return Deck.objects.get(pk=self.deck_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pk'] = self.deck_id
        return context

    def get_success_url(self):
        return reverse_lazy('decks')


class CardDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_card_deletion.html'

    @property
    def deck_id(self):
        return self.kwargs['pk']

    @property
    def card_id(self):
        return self.kwargs['card_pk']

    def get_object(self, queryset=None):
        return Flashcard.objects.get(id=self.card_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pk'] = self.deck_id
        context['card_pk'] = self.card_id
        return context

    def get_success_url(self):
        return reverse_lazy('deck-detail', kwargs={'pk': self.deck_id})


class CardUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['front_text', 'back_text']
    template_name = 'update_card.html'

    @property
    def deck_id(self):
        return self.kwargs['pk']

    @property
    def card_id(self):
        return self.kwargs['card_pk']

    def get_object(self, queryset=None):
        return Flashcard.objects.get(id=self.card_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pk'] = self.deck_id
        context['card_pk'] = self.card_id
        return context

    def get_success_url(self):
        return reverse_lazy('deck-detail', kwargs={'pk': self.deck_id})


class UserDecksView(LoginRequiredMixin, TemplateView):
    template_name = 'user_decks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['decks'] = Deck.objects.all()
        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Flashcard
    fields = ['front_text', 'back_text']
    template_name = 'create_card.html'

    @property
    def deck_id(self):
        return self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pk'] = self.deck_id
        return context

    def form_valid(self, form):
        deck_form: Flashcard = form.instance
        deck_form.last_seen_date = datetime.now()
        deck_form.parent_deck = Deck.objects.get(pk=self.deck_id)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck-detail', kwargs={'pk': self.deck_id})


class DeckDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'deck_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deck = Deck.objects.get(pk=context['pk'])
        context['title'] = deck.title
        context['cards'] = deck.flashcards.all()
        context['deck'] = deck

        return context


class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    fields = ['title']
    template_name = 'create_deck.html'

    def form_valid(self, form):
        deck_form: Deck = form.instance
        deck_form.owner = self.request.user
        deck_form.last_seen_date = datetime.now()

        return super().form_valid(form)


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


