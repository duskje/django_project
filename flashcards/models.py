from django.db import models
from django.conf import settings


class Deck(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='decks',
    )

    title = models.CharField(max_length=200)
    last_seen_date = models.DateTimeField()


class Flashcard(models.Model):
    parent_deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='flashcards',
    )

    last_seen_date = models.DateTimeField()

    front_text = models.CharField(max_length=200)
    back_text = models.CharField(max_length=200)
