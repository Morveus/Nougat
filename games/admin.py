from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Game, Genre

class GameAdminSite(AdminSite):
    site_header = 'Games List Administration'
    site_title = 'Games List Admin'
    index_title = 'Games List Administration'

game_admin_site = GameAdminSite(name='game_admin')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'genre', 'release_year', 'number_of_players')
    list_filter = ('platform', 'genre', 'release_year')
    search_fields = ('title', 'genre__name')

# Register the models with our custom admin site
game_admin_site.register(Game, GameAdmin)
game_admin_site.register(Genre, GenreAdmin)
game_admin_site.register(User, UserAdmin)
game_admin_site.register(Group, GroupAdmin)
