from django.core.management.base import LabelCommand
from movies.utils import import_tmdb

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Imports a tmdb movie from its id """
        import_tmdb(label)
