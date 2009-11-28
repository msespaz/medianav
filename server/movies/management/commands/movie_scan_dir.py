from django.core.management.base import LabelCommand
from movies.utils import import_tmdb, scan_directory
from django.conf import settings
import os
from movies.models import VideoDirectory

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Scan a directory """
        if label == 'all':
            # Scan all directories in the movie media directory
            for directory in os.listdir(settings.MEDIANAV_MOVIE_DIR):
                if os.path.isdir(os.path.join(settings.MEDIANAV_MOVIE_DIR, directory)):
                    scan_directory(os.path.join(settings.MEDIANAV_MOVIE_DIR, directory))
            # Scan the database and remove directories that do not exist
            for directory in VideoDirectory.objects.all():
                if not os.path.isdir(os.path.join(settings.MEDIANAV_MOVIE_DIR, directory.name)):
                    print "DBFIX: Removing Directory %s" % directory.name
                    for file in directory.movievideofile_set.all():
                        print "DBFIX:     Removing File %s" % file.name 
                        file.delete()
                    directory.delete()

        else:
            scan_directory(label)
