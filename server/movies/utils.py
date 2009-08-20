# Utility functions for the movie database

from movies.models import *
import themoviedb
from django.conf import settings
import datetime
import os
import urllib
import re

def scan_directory(directory):
    """ Scans a directory to find the movie name """
    head, tail = os.path.split(os.path.abspath(directory))
    if tail:
        movie_dir = tail
    else:
        movie_dir = head
    print 'Processing', movie_dir
    imdbid = None
    videofilenames = []
    for filename in os.listdir(directory):
        if filename == 'moviedb.imdb':
            id = open(os.path.join(directory, filename), 'r').read().strip()
            print '    Found moviedb.imdb with id [%s]' % id
            imdbid = 'tt%s' % id
        if os.path.splitext(filename)[1].lower() == '.nfo':
            nfo = open(os.path.join(directory, filename), 'r').read()
            p = re.compile('tt[0-9]+', re.MULTILINE)
            m = p.findall(nfo)
            if len(m)>0:
                imdbid = m[0]
                print '    Found nfo file %s with id [%s]' % (filename, imdbid)
            p = re.compile('Title\?[0-9]+', re.MULTILINE)
            m = p.findall(nfo)
            if len(m)>0:
                imdbid = m[0].replace('Title?', 'tt')
                print '    Found nfo file %s with id [%s]' % (filename, imdbid)
        if os.path.splitext(filename)[1].lower() in settings.MEDIA_EXTENSIONS:
            print '    Found media file [%s]' % filename
            videofilenames.append(filename)
    tmdb = themoviedb.TheMovieDB(settings.TMDBAPI_KEY)
    if imdbid:
        if Movie.objects.filter(imdb_id=imdbid).count()<1:
            try:
                print '    Looking up movie from imdbid'
                movie = tmdb.movie_imdblookup(imdbid)
                if movie.name:
                    print '    Found match', movie.id, movie.name
                    import_tmdb(movie.id)
            except:
                pass   # TODO: Fix this up to handle only known errors
        else:
            print '    Movie already in database'

def import_tmdb(id):
    """ Import a movie from The Movie DB """
    tmdb = themoviedb.TheMovieDB(settings.TMDBAPI_KEY)
    tmdbmovie = tmdb.movie_getinfo(id)
    print 'Imporing', tmdbmovie.name
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


