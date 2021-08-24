from django.db import models


class Deck(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=25)
    last_seen_date = models.DateTimeField()


class Flashcard(models.Model):
    parent_deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    last_seen_date = models.DateTimeField()

    front_text = models.CharField(max_length=200)
    back_text = models.CharField(max_length=200)
