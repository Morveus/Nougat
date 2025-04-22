from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Game, Genre
from .forms import GameForm

# Create your views here.

class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique platforms from games
        context['platforms'] = sorted(set(game.platform for game in context['games']))
        # Get all genres
        context['genres'] = Genre.objects.all().order_by('name')
        # Add has_image filter for admin users
        if self.request.user.is_staff:
            context['show_image_filter'] = True
        return context

class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('game-list')
    login_url = '/admin/login/'

    def get_initial(self):
        initial = super().get_initial()
        # Get last selected platform and genre from session
        last_platform = self.request.session.get('last_platform')
        last_genre = self.request.session.get('last_genre')
        
        if last_platform:
            initial['platform'] = last_platform
        if last_genre:
            initial['genre'] = last_genre
            
        return initial

    def form_valid(self, form):
        # Store the selected platform and genre in session
        self.request.session['last_platform'] = form.cleaned_data['platform']
        self.request.session['last_genre'] = form.cleaned_data['genre'].id
        return super().form_valid(form)

class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('game-list')
    login_url = '/admin/login/'

class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = 'games/game_confirm_delete.html'
    success_url = reverse_lazy('game-list')
    login_url = '/admin/login/'