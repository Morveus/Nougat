from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('new/', views.GameCreateView.as_view(), name='game-create'),
    path('<int:pk>/edit/', views.GameUpdateView.as_view(), name='game-update'),
    path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game-delete'),
    path('ai-game-info/', views.AIGameInfoView.as_view(), name='ai-game-info'),
    path('api-key/', views.APIKeyView.as_view(), name='api-key'),
] 