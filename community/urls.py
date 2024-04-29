from django.urls import path
from . import views

urlpatterns = [
    path('', views.default_community),
    path('<group>/', views.community, name='community'),
]
