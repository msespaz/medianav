from django.core.management.base import LabelCommand
from movies.utils import import_tmdb
from movies.models import Movie

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Imports a tmdb movie from its imdb id """
        if label == 'all':
            for movie in Movie.objects.filter(moviedb_last_updated__isnull=True):
		print "Updating [%s] %s" % (movie.imdb_id, movie.title)
                import_tmdb(movie.imdb_id)
        else:
            import_tmdb(label)
