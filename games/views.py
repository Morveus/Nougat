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
import openai
from .models import Game, Genre, UserAPIKey
from .forms import GameForm, APIKeyForm

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

class APIKeyView(LoginRequiredMixin, FormView):
    template_name = 'games/api_key_form.html'
    form_class = APIKeyForm
    success_url = reverse_lazy('game-list')

    def get_object(self):
        try:
            return UserAPIKey.objects.get(user=self.request.user)
        except UserAPIKey.DoesNotExist:
            return None

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

    def form_valid(self, form):
        api_key = form.save(commit=False)
        api_key.user = self.request.user
        api_key.save()
        messages.success(self.request, _('Your API key has been saved successfully.'))
        return super().form_valid(form)

@method_decorator(require_POST, name='dispatch')
class AIGameInfoView(LoginRequiredMixin, View):
    def post(self, request):
        title = request.POST.get('title', '')
        if not title:
            return JsonResponse({'error': str(_('Title is required'))}, status=400)

        try:
            # Get user's API key
            try:
                user_api_key = UserAPIKey.objects.get(user=request.user)
                api_key = user_api_key.openai_api_key
            except UserAPIKey.DoesNotExist:
                return JsonResponse({
                    'error': str(_('Please set your OpenAI API key first.')),
                    'redirect': str(reverse_lazy('api-key'))
                }, status=400)

            # Initialize OpenAI client with user's API key
            openai.api_key = api_key
            
            # Create a prompt for the AI
            prompt = f"""Given the game title "{title}", provide the following information in JSON format:
            - platform (from this list: Microsoft Windows, Sony PlayStation 5, Sony PlayStation 4, Sony PlayStation 3, Sony PlayStation 2, Sony PlayStation, Microsoft Xbox Series X/S, Microsoft Xbox One, Nintendo Switch, Nintendo Wii U, Nintendo Wii, Nintendo GameCube, Nintendo Game Boy Advance, Nintendo Game Boy Color, Nintendo Game Boy, Nintendo DS, Nintendo 3DS, Nintendo 64, Nintendo NES, Nintendo SNES, Other)
            - genre (from existing genres in the database)
            - release_year (as a number)
            - number_of_players (as a number)
            - description (a brief description of the game)
            - lan_playable (true or false)
            - notes (any additional interesting information)
            """

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides information about video games."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the response
            content = response.choices[0].message.content
            # Extract JSON from the response
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                game_info = json.loads(json_match.group())
                
                # Get or create genre
                genre_name = game_info.get('genre', '')
                genre, created = Genre.objects.get_or_create(name=genre_name)
                
                # Prepare response data
                data = {
                    'platform': game_info.get('platform', ''),
                    'genre': genre.id,
                    'release_year': game_info.get('release_year', ''),
                    'number_of_players': game_info.get('number_of_players', 1),
                    'description': game_info.get('description', ''),
                    'lan_playable': game_info.get('lan_playable', False),
                    'notes': game_info.get('notes', '')
                }
                
                return JsonResponse(data)
            else:
                return JsonResponse({'error': str(_('Could not parse AI response'))}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
