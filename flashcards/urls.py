from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('decks/', views.UserDecksView.as_view(), name='decks'),
    path('decks/add/', views.DeckCreateView.as_view(), name='deck-add'),
    path('deck/<int:pk>/cards/', views.DeckDetailView.as_view(), name='deck-detail'),
    path('deck/<int:pk>/update/', views.DeckUpdateView.as_view(), name='deck-update'),
    path('deck/<int:pk>/delete/', views.DeckDeleteView.as_view(), name='deck-delete'),

    path('deck/<int:pk>/review_flashcards/', views.flashcards_review_view, name='deck-review'),

    path('deck/<int:pk>/add_card/', views.CardCreateView.as_view(), name='card-add'),
    path('deck/<int:pk>/card/<int:card_pk>/', views.CardUpdateView.as_view(), name='card-update'),
    path('deck/<int:pk>/card/<int:card_pk>/confirm_delete/', views.CardDeleteView.as_view(), name='card-delete'),
]