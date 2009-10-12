from django.core.management.base import LabelCommand
from movies.utils import import_imdb, scan_directory
from movies.models import Movie, VideoDirectory
from movies.imdb import IMDb
from django.conf import settings
import os

class Command(LabelCommand):
    def handle_label(sself, label, **options):
        """ Searches for an imdb movie by title for all directories without an associated movie """
        dirs = VideoDirectory.objects.filter(movie__id__isnull=True)
        imdb = IMDb('http', useModule='BeautifulSoup')
        for dir in dirs:
            name = dir.name.split(')')[0]+')'
            print '-'*20
            print name
            print '-'*20
            s=imdb.search_movie(name)
            for index, r in enumerate(s):
                print "%2d %s - %s (%s) %s" % (index, r.movieID, r['title'], r['year'], r['kind'])
            choice = raw_input('Index [0]: ')
            if choice == '':
                index = 0
            else:
                index = int(choice)
            print 'You chose %d' % index
            if index > -1:
                filename = os.path.join(settings.MEDIANAV_MOVIE_DIR, dir.name, 'moviedb.imdb')
                print 'Writing %s to %s ' % (s[index].movieID, filename)
                f = open(filename, 'w')
                f.write('%s' % s[index].movieID)
                f.close()
                scan_directory(os.path.join(settings.MEDIANAV_MOVIE_DIR, dir.name))
            else:
                print 'Skipping'

