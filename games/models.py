from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import os
from .fields import CompressedImageField

def game_image_path(instance, filename):
    # Get the first character of the filename
    first_char = filename[0].lower()
    # Create the path: uploads/first_char/filename
    return os.path.join('uploads', first_char, filename)


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Game(models.Model):
    PLATFORM_CHOICES = [
        ('Microsoft Windows', 'Microsoft Windows'),
        ('Linux', 'Linux'),
        ('Mac', 'Mac'),
        ('Sony PlayStation 5', 'Sony PlayStation 5'),
        ('Sony PlayStation 4', 'Sony PlayStation 4'),
        ('Sony PlayStation 3', 'Sony PlayStation 3'),
        ('Sony PlayStation 2', 'Sony PlayStation 2'),
        ('Sony PlayStation', 'Sony PlayStation'),
        ('Microsoft Xbox Series X/S', 'Microsoft Xbox Series X/S'),
        ('Microsoft Xbox One', 'Microsoft Xbox One'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('Nintendo Wii U', 'Nintendo Wii U'),
        ('Nintendo Wii', 'Nintendo Wii'),
        ('Nintendo GameCube', 'Nintendo GameCube'),
        ('Nintendo Game Boy Advance', 'Nintendo Game Boy Advance'),
        ('Nintendo Game Boy Color', 'Nintendo Game Boy Color'),
        ('Nintendo Game Boy', 'Nintendo Game Boy'),
        ('Nintendo DS', 'Nintendo DS'),
        ('Nintendo 3DS', 'Nintendo 3DS'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('Nintendo Wii U', 'Nintendo Wii U'),
        ('Nintendo 64', 'Nintendo 64'),
        ('Nintendo NES', 'Nintendo NES'),
        ('Nintendo SNES', 'Nintendo SNES'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES, verbose_name=_("Platform"))
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name=_("Genre"))
    release_year = models.IntegerField(verbose_name=_("Release Year"), null=True, blank=True)
    number_of_players = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Number of Players"),
        help_text=_("Minimum number of players required")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A brief description of the game")
    )
    lan_playable = models.BooleanField(
        default=False,
        verbose_name=_("LAN Playable"),
        help_text=_("Whether the game supports LAN multiplayer")
    )
    image = CompressedImageField(
        upload_to=game_image_path,
        verbose_name=_("Game Image"),
        null=True,
        blank=True,
        max_width=1200,
        max_height=1200,
        quality=80
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ['title']

    def __str__(self):
        return self.title
