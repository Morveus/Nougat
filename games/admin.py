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

class HasImageFilter(admin.SimpleListFilter):
    title = 'Image Status'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has image'),
            ('no', 'No image'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image__isnull=True).exclude(image='')
        if self.value() == 'no':
            return queryset.filter(image__isnull=True) | queryset.filter(image='')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'genre', 'release_year', 'number_of_players', 'has_image')
    list_filter = ('platform', 'genre', 'release_year', HasImageFilter)
    search_fields = ('title', 'genre__name')

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

# Register the models with our custom admin site
game_admin_site.register(Game, GameAdmin)
game_admin_site.register(Genre, GenreAdmin)
game_admin_site.register(User, UserAdmin)
game_admin_site.register(Group, GroupAdmin)
