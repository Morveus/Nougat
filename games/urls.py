from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('create/', views.GameCreateView.as_view(), name='game-create'),
    path('<int:pk>/update/', views.GameUpdateView.as_view(), name='game-update'),
    path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game-delete'),
    path('api-key/', views.APIKeyView.as_view(), name='api-key'),
    path('ai-game-info/', views.AIGameInfoView.as_view(), name='ai-game-info'),
    path('<int:pk>/detail/', views.GameDetailView.as_view(), name='game-detail'),
] 