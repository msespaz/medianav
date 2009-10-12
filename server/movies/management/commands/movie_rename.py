from django.core.management.base import LabelCommand
from movies.utils import import_imdb, scan_directory
from movies.models import Movie, VideoDirectory
from movies.imdb import IMDb
from django.conf import settings
import os

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Renames all the directories to a formatted name """
        dirs = VideoDirectory.objects.filter(movie__id__isnull=False)
        for dir in dirs:
            new_name = dir.format_name()
            if dir.name != new_name:
                old_name = dir.name
                try:
                    os.rename(os.path.join(settings.MEDIANAV_MOVIE_DIR, old_name), os.path.join(settings.MEDIANAV_MOVIE_DIR, new_name))
                    dir.name = new_name
                    dir.save()
                    print 'Renamed [%s] to [%s]' % (old_name, new_name)
                except:
                    print 'FAILED [%s] to [%s]' % (old_name, new_name)
