from django.core.management.base import LabelCommand
from movies.utils import import_tmdb, scan_directory
import os

movies_dir = '/data/movies/all'

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Scan a directory """
        if label == 'all':
            for directory in os.listdir(movies_dir):
                if os.path.isdir(os.path.join(movies_dir, directory)):
                    scan_directory(os.path.join(movies_dir, directory))
        else:
            scan_directory(label)
