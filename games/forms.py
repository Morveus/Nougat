from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Game, Genre

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'platform', 'genre', 'release_year', 
                 'number_of_players', 'description', 'lan_playable',
                 'image', 'notes']
        widgets = {
            'release_year': forms.NumberInput(attrs={'min': 1970, 'max': 2100}),
            'number_of_players': forms.NumberInput(attrs={'min': 1}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'data-drag-drop': 'true'
            }),
        }
        labels = {
            'title': _('Title'),
            'platform': _('Platform'),
            'genre': _('Genre'),
            'release_year': _('Release Year'),
            'number_of_players': _('Number of Players'),
            'description': _('Description'),
            'lan_playable': _('LAN Playable'),
            'image': _('Game Image'),
            'notes': _('Notes'),
        }
        help_texts = {
            'number_of_players': _('Minimum number of players required'),
            'release_year': _('Enter the year of release'),
            'description': _('A brief description of the game'),
            'lan_playable': _('Whether the game supports LAN multiplayer'),
            'image': _('Drag and drop an image here or click to select'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for genre to ensure it's ordered
        self.fields['genre'].queryset = Genre.objects.all().order_by('name')