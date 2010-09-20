from django.core.management.base import LabelCommand
from movies.utils import import_imdb
from movies.models import Movie
from movies.imdb import IMDb

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Searches for an imdb movie by title """
        imdb = IMDb()
        s=imdb.search_movie(label)
        for r in s:
            print "%s - %s (%s)" % (r.movieID, r['title'], r['year'])
