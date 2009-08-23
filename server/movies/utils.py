# Utility functions for the movie database

from movies.models import *
import themoviedb
from django.conf import settings
import datetime
import os
import stat
import urllib
import re
from movies.imdb import IMDb

def scan_directory(directory):
    """ Scans a directory, adds it to the database with its files and associates it to a movie 
        The movie is identified by its imdb id, which can either be in a moviedb.imdb file
        or a URL present in an nfo file in the directory """
   
    # Works out the actual movie directory name if a long path was passed
    # This assumes one movie per directory and that the last part of the path is the movie directory
    head, tail = os.path.split(os.path.abspath(directory))
    if tail:
        movie_dir = tail
    else:
        movie_dir = head

    print 'Processing', movie_dir

    # Check first if this directory is in the database already
    try:
        videodirectory = VideoDirectory.objects.get(name=movie_dir)
    except VideoDirectory.DoesNotExist:
        print "Creating new directory in database"
        videodirectory = VideoDirectory(name=movie_dir)

    # Update basic fields
    s=os.stat(directory)
    videodirectory.ctime=datetime.datetime.fromtimestamp(s[stat.ST_CTIME])
    videodirectory.last_updated = datetime.datetime.now()

    # This finds the imdb id, if present
    imdbid = None
    videofilenames = []
    for filename in os.listdir(directory):
        if filename == 'moviedb.imdb':
            id = open(os.path.join(directory, filename), 'r').read().strip()
            print '    Found moviedb.imdb with id [%s]' % id
            imdbid = '%s' % id
        if os.path.splitext(filename)[1].lower() == '.nfo':
            nfo = open(os.path.join(directory, filename), 'r').read()
            p = re.compile('tt[0-9]+', re.MULTILINE)
            m = p.findall(nfo)
            if len(m)>0:
                imdbid = m[0].replace('tt','')
                print '    Found nfo file %s with id [%s]' % (filename, imdbid)
            p = re.compile('Title\?[0-9]+', re.MULTILINE)
            m = p.findall(nfo)
            if len(m)>0:
                imdbid = m[0].replace('Title?', '')
                print '    Found nfo file %s with id [%s]' % (filename, imdbid)
        if os.path.splitext(filename)[1].lower() in settings.MEDIA_EXTENSIONS:
            print '    Found media file [%s]' % filename
            videofilenames.append(filename)

    # If there is an imdb, link it to a movie, or create a new one to link it to
    if imdbid:
        try:
            movie = Movie.objects.get(imdb_id = imdbid)
            print "Linking to existing movie"
        except Movie.DoesNotExist:
            print "Creating new movie to link to"
            movie = Movie(imdb_id=imdbid, title=movie_dir)
            movie.save()
        videodirectory.movie=movie
    else:
        print 'No imdbid found'

    # Save the directory database entry
    videodirectory.save()

    # TODO: Update the list of media files in the database

def find_or_create_person(pi):
    """ Finds or creates a person from an imdb person object """
    try:
        pm = Person.objects.get(imdb_id = pi.personID)
    except Person.DoesNotExist:
        print "Creating new person", pi['name']
        pm = Person(imdb_id = pi.personID, name=pi['name'])
        pm.save()
    return pm

def import_imdb(id):
    """ Import a movie from IMDB """
    imdb = IMDb('http', useModule='BeautifulSoup')
    print 'Importing from imdb', id
    mi=imdb.get_movie(id) # mi is the movie from imdb
    if mi:
        print "Found movie", mi['title']
        # Try to find a match in our database mm is the movie from medianav
        try:
            mm = Movie.objects.get(imdb_id = mi.movieID)
        except Movie.DoesNotExist:
            print "Creating new movie"
            mm = Movie(imdb_id = mi.movieID, title=mi['title'])
            mm.save()
        # Update the movie with information from imdb
        mm.imdb_last_updated = datetime.datetime.now()
        mm.title = mi['title']
        mm.imdb_long_title = mi['long imdb title']
        mm.canon_title = mi['canonical title']
        mm.imdb_canon_long_title = mi['long imdb canonical title']
        mm.year = mi['year']
        mm.imdb_kind = mi['kind']
        if mi.has_key('cover url'):
            mm.imdb_cover_url = mi['cover url']
        if mi.has_key('plot'):
            # These are user contributed plots, not always available
            mm.plot = mi['plot'][0] # Save the first plot returned
        if mi.has_key('plot outline'):
            mm.plot_outline = mi['plot outline']
        mm.imdb_rating = mi['rating']
        mm.imdb_votes = mi['votes']
        if mi.has_key('mpaa'):
            mm.mpaa = mi['mpaa']
        if mi.has_key('runtimes'):
            mm.runtime = int(re.sub('[^0-9]+', '', mi['runtimes'][0])) # Pick the first runtime

        if mi.has_key('imdbIndex'):
            mm.imdb_index = mi['imdbIndex']

        # Process the crew

        for crewjob in ('director', 'writer', 'composer'):
            order = 1
            if mi.has_key(crewjob):
                for pi in mi[crewjob]:
                    pm = find_or_create_person(pi)
                    try:
                        # See if this crew alread exist by maching person, movie and job
                        cast = Cast.objects.get(person=pm, movie=mm, job=crewjob)
                    except Cast.DoesNotExist:
                        print 'Creating new crew member', pm.name, crewjob
                        cast = Cast(person=pm, movie=mm, job=crewjob, bill_order=order)
                        cast.save()
                    order += 1
                
        # Process actors
        if mi.has_key('cast'):
            order = 1
            for pi in mi['cast']:
                pm = find_or_create_person(pi)
                from types import ListType
                if isinstance(pi.currentRole, ListType):
                    role = ' | '.join([c['name'] for c in pi.currentRole])
                elif pi.currentRole.has_key('name'):
                    role = pi.currentRole['name']
                else:
                    role = 'uncredited'
                try:
                    # See if this cast/crew alread exist by maching person, movie and job and role
                    cast = Cast.objects.get(person=pm, movie=mm, job='actor', role=role)
                except Cast.DoesNotExist:
                    print 'Creating new cast member', pm.name, role
                    cast = Cast(person=pm, movie=mm, job='actor', role=role, bill_order=order)
                    cast.save()
                order += 1

        # Process country list
        if mi.has_key('countries'):
            for ci in mi['countries']:
                try:
                    country = Country.objects.get(name=ci)
                except Country.DoesNotExist:
                    print 'Creating new country', ci
                    country = Country(name=ci) 
                    country.save()
                mm.countries.add(country)

        # Process genre list
        for gi in mi['genres']:
            try:
                genre = Genre.objects.get(name=gi)
            except Genre.DoesNotExist:
                print 'Creating new genre', gi
                genre = Genre(name=gi) 
                genre.save()
            mm.genres.add(genre)

        # Process language list
        if mi.has_key('languages'):
            for li in mi['languages']:
                try:
                    language = Language.objects.get(name=li)
                except Language.DoesNotExist:
                    print 'Creating new language', li
                    language = Language(name=li) 
                    language.save()
                mm.languages.add(language)

        # Process certificate list
        if mi.has_key('certificates'):
            for ci in mi['certificates']:
                # Strip off the note section
                name = ci.split('::')[0]
                try:
                    certificate = Certificate.objects.get(name=name)
                except Certificate.DoesNotExist:
                    print 'Creating new certificate', name
                    certificate = Certificate(name=name) 
                    certificate.save()
                mm.certificates.add(certificate)

        # Process production companies
        if mi.has_key('production companies'):
            for ci in mi['production companies']:
                try:
                    company = Company.objects.get(imdb_id=ci.companyID)
                except Company.DoesNotExist:
                    print 'Creating new production company', ci['name'] 
                    company = Company(name=ci['name'], imdb_id=ci.companyID) 
                    company.save()
                mm.production_companies.add(company)

        # Save the medianav movie entry to the database
        mm.save()

def import_tmdb(imdbid):
    """ Import a movie from The Movie DB, based on its imdb id
        this is only used to fill in a few extra fields and to get
        the poster and backdrop images """
    tmdb = themoviedb.TheMovieDB(settings.TMDBAPI_KEY)
    try:
        tmdbmovie = tmdb.movie_imdblookup('tt' + imdbid)
    except:
        print "Error retrieving data from tmdb"
        return
    try:
        movie = Movie.objects.get(imdb_id = imdbid)
        print "Updating existing movie"
    except Movie.DoesNotExist:
        print "Creating new movie"
        movie = Movie(imdb_id = imdbid)
        movie.save
    print 'Movie: %s' % movie.title
    if tmdbmovie.name:
        print 'Importing', tmdbmovie.name
        if tmdbmovie.trailer:
            movie.trailer_url = tmdbmovie.trailer
        movie.moviedb_id = tmdbmovie.id
        movie.moviedb_rating = float(tmdbmovie.rating)
        movie.moviedb_url = tmdbmovie.url
        movie.moviedb_last_updated = datetime.datetime.now()
        for i in tmdbmovie.images:
            if i.type=='poster' and i.size=='original':
                movie.moviedb_poster_url = i.url
            if i.type=='backdrop' and i.size=='original':
                movie.moviedb_backdrop_url = i.url
        movie.save()
        # Download imagees
        if movie.moviedb_poster_url:
            filename = "%s/img/poster/%s.jpg" % (settings.MEDIANAV_MOVIES_MEDIA, movie.moviedb_id)
            if not os.access(filename, os.F_OK):
                print "Downloading poster image to %s" % (filename)
                urllib.urlretrieve(movie.moviedb_poster_url, filename)
        if movie.moviedb_backdrop_url:
            filename = "%s/img/backdrop/%s.jpg" % (settings.MEDIANAV_MOVIES_MEDIA, movie.moviedb_id)
            if not os.access(filename, os.F_OK):
                print "Downloading backdsrop image to %s" % (filename)
                urllib.urlretrieve(movie.moviedb_backdrop_url, filename)
    else:
        print 'No tmdb match found'

def import_tmdb_old(id):
    """ Import a movie from The Movie DB """
    tmdb = themoviedb.TheMovieDB(settings.TMDBAPI_KEY)
    tmdbmovie = tmdb.movie_getinfo(id)
    print 'Importing', tmdbmovie.name
    try:
        movie = Movie.objects.get(moviedb_id = int(tmdbmovie.id))
        print "Updating existing movie"
    except Movie.DoesNotExist:
        print "Creating new movie"
        movie = Movie(moviedb_id = int(tmdbmovie.id))

    movie.name = tmdbmovie.name
    #movie.status
    #movie.watched
    movie.overview = tmdbmovie.overview
    movie.release = tmdbmovie.released
    movie.runtime = int(tmdbmovie.runtime)
    movie.trailer_url = tmdbmovie.trailer
    movie.homepage = tmdbmovie.homepage
    movie.imdb_id = tmdbmovie.imdb_id
    movie.moviedb_rating = float(tmdbmovie.rating)
    movie.moviedb_url = tmdbmovie.url
    movie.moviedb_last_updated = datetime.datetime.now()
    for i in tmdbmovie.images:
        if i.type=='poster' and i.size=='original':
            movie.moviedb_poster_url = i.url
        if i.type=='backdrop' and i.size=='original':
            movie.moviedb_backdrop_url = i.url

    movie.save()


    # Update the genres
    for c in tmdbmovie.categories:
        if c.type == 'genre':
            try:
                genre = Genre.objects.get(name=c.name)
            except Genre.DoesNotExist:
                genre = Genre(name = c.name, moviedb_id = c.id)
                genre.save()
            movie.genres.add(genre)

    #movie.cast
    for p in tmdbmovie.cast:
        try:
            person = Person.objects.get(moviedb_id=p.id)
        except Person.DoesNotExist:
            person = Person(name=p.name, moviedb_id=p.id)
            person.save()
        #p.job, p.url, p.name, p.character, p.id
        try:
            cast = Cast.objects.get(person=person, movie=movie, job=p.job)
        except Cast.DoesNotExist:
            cast = Cast(person=person, movie=movie, character=p.character, job=p.job)
            cast.save()
    
    #movie.studios
    for s in tmdbmovie.studios:
        try:
            studio = Studio.objects.get(moviedb_id=s.id)
        except Studio.DoesNotExist:
            studio = Studio(name = s.name, moviedb_id = s.id)
            studio.save()
        movie.studios.add(studio)

    #movie.countries
    for c in tmdbmovie.countries:
        try:
            country = Country.objects.get(moviedb_id=c.id)
        except Country.DoesNotExist:
            country = Country(name = c.name, moviedb_id = c.id) 
            country.save()
        movie.countries.add(country)
    
    # Download images
    filename = "%s/img/poster/%s.jpg" % (settings.MEDIANAV_MOVIES_MEDIA, movie.moviedb_id)
    if not os.access(filename, os.F_OK):
        print "Downloading poster image to %s" % (filename)
        urllib.urlretrieve(movie.moviedb_poster_url, filename)
    filename = "%s/img/backdrop/%s.jpg" % (settings.MEDIANAV_MOVIES_MEDIA, movie.moviedb_id)
    if not os.access(filename, os.F_OK):
        print "Downloading backdsrop image to %s" % (filename)
        urllib.urlretrieve(movie.moviedb_backdrop_url, filename)

