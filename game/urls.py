from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='game'),
    path('flashcard/', views.flashcard_levels, name='flashcard_levels'),
    path('flashcard/<int:level>', views.flashcard, name='flashcard'),
    path('ordering/', views.ordering_levels, name='ordering_levels'),
    path('ordering/alphabet/', views.ordering_alphabet, name='ordering_alphabet'),
    path('ordering/image/', views.ordering_image, name='ordering_image'),
    path('quiz/', views.quiz_levels, name='quiz_levels'),
    path('quiz/normal/<int:level>', views.quiz_normal, name='quiz_normal'),
    path('quiz/ai', views.quiz_ai_main, name='quiz_ai_main'),
    path('quiz/ai/predictor', views.quiz_ai, name='quiz_ai'),
]
