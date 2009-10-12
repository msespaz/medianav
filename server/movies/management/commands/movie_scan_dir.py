from django.core.management.base import LabelCommand
from movies.utils import import_tmdb, scan_directory
from django.conf import settings
import os

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Scan a directory """
        if label == 'all':
            for directory in os.listdir(settings.MEDIANAV_MOVIE_DIR):
                if os.path.isdir(os.path.join(settings.MEDIANAV_MOVIE_DIR, directory)):
                    scan_directory(os.path.join(settings.MEDIANAV_MOVIE_DIR, directory))
        else:
            scan_directory(label)
