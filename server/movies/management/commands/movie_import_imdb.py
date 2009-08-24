from django.core.management.base import LabelCommand
from movies.utils import import_imdb
from movies.models import Movie

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Imports a imdb movie from its id """
        if label == 'all':
            for movie in Movie.objects.filter(imdb_last_updated__isnull=True):
                import_imdb(movie.imdb_id)
        else:
            import_imdb(label)
