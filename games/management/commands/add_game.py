from django.core.management.base import BaseCommand
from games.models import Game, Genre

class Command(BaseCommand):
    help = 'Add a new game to the database'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('platform', type=str)
        parser.add_argument('genre', type=str)
        parser.add_argument('--release-year', type=int)
        parser.add_argument('--players', type=int, default=1)
        parser.add_argument('--lan', action='store_true')
        parser.add_argument('--description', type=str, help='A brief description of the game')

    def handle(self, *args, **options):
        # Get or create genre
        genre, _ = Genre.objects.get_or_create(name=options['genre'])
        
        # Create game
        game = Game.objects.create(
            title=options['title'],
            platform=options['platform'],
            genre=genre,
            release_year=options['release_year'],
            number_of_players=options['players'],
            lan_playable=options['lan'],
            description=options['description']
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created game "{game.title}"'))