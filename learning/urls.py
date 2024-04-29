from django.urls import path
from . import views

urlpatterns = [
    path('', views.learning, name='learning'),
    path('answer/', views.answer, name='get_answer'),
    
]
