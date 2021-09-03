from django.urls import path

from django.contrib.auth import views as auth_views
from .views import RegisterView, UserDecksView, DeckDetailView, DeckCreateView, CardCreateView, flashcards_review_view, \
    CardUpdateView, CardDeleteView, DeckUpdateView, DeckDeleteView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('decks/', UserDecksView.as_view(), name='decks'),
    path('add_deck/', DeckCreateView.as_view(), name='deck-add'),
    path('deck/<int:pk>/cards/', DeckDetailView.as_view(), name='deck-detail'),
    path('deck/<int:pk>/update/', DeckUpdateView.as_view(), name='deck-update'),
    path('deck/<int:pk>/delete/', DeckDeleteView.as_view(), name='deck-delete'),

    path('deck/<int:pk>/review_flashcards/', flashcards_review_view, name='deck-review'),

    path('deck/<int:pk>/add_card/', CardCreateView.as_view(), name='card-add'),
    path('deck/<int:pk>/card/<int:card_pk>/', CardUpdateView.as_view(), name='card-update'),
    path('deck/<int:pk>/card/<int:card_pk>/confirm_delete/', CardDeleteView.as_view(), name='card-delete'),
]