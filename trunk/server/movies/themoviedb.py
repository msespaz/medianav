#!/usr/bin/python

import urllib

import xml.etree.cElementTree as ET

class TheMovieDB(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.themoviedb.org/2.1'

    def tmdb_method(self, method, value):
        # TODO: use urllib.urlencode for the value
        method_url = '%s/%s/en/xml/%s/%s' % (self.base_url, method, self.api_key, value)
        data = urllib.urlopen(method_url).read()
        et = ET.fromstring(data)
        return et

    class Category(object):
        def __init__(self, node):
            self.type = node.get('type')
            self.url = node.get('url')
            self.name = node.get('name')
            self.id = int(self.url.split('/')[-1])

    class Studio(object):
        def __init__(self, node):
            self.url = node.get('url')
            self.name = node.get('name')
            self.id = int(self.url.split('/')[-1])

    class Country(object):
        def __init__(self, node):
            self.url = node.get('url')
            self.name = node.get('name')
            self.code = node.get('code')
            self.id = int(self.url.split('/')[-1])

    class Person(object):
        def __init__(self, node):
            self.job = node.get('job')
            self.url = node.get('url')
            self.name = node.get('name')
            self.character = node.get('character')
            self.id = node.get('id')

    class Image(object):
        def __init__(self, node):
            self.type = node.get('type')
            self.size = node.get('size')
            self.url = node.get('url')
            self.id = node.get('id')

    class Movie(object):
        def __init__(self, node):
            self.name = node.findtext('name')
            self.popularity = node.findtext('popularity')
            self.alternative_name = node.findtext('alternative_name')
            self.type = node.findtext('type')
            self.id = node.findtext('id')
            self.imdb_id = node.findtext('imdb_id')
            self.url = node.findtext('url')
            self.overview = node.findtext('overview')
            self.rating = node.findtext('rating')
            self.released = node.findtext('released')
            self.runtime = node.findtext('runtime')
            self.budget = node.findtext('budget')
            self.revenue = node.findtext('revenue')
            self.homepage = node.findtext('homepage')
            self.trailer = node.findtext('trailer')
            self.categories = []
            if node.find('categories'):
                for n in node.find('categories'):
                    self.categories.append(TheMovieDB.Category(n)) 
            self.studios = []
            if node.find('studios'):
                for n in node.find('studios'):
                    self.studios.append(TheMovieDB.Studio(n)) 
            self.countries = []
            if node.find('countries'):
                for n in node.find('countries'):
                    self.countries.append(TheMovieDB.Country(n)) 
            self.images = []
            if node.find('images'):
                for n in node.find('images'):
                    self.images.append(TheMovieDB.Image(n)) 
            self.cast = []
            if node.find('cast'):
                for n in node.find('cast'):
                    self.cast.append(TheMovieDB.Person(n)) 

    def movie_getinfo(self, movie_id):
        tree = self.tmdb_method('Movie.getInfo', movie_id)
        movie_node = tree.find('movies')[0]
        return TheMovieDB.Movie(movie_node)
    
    def movie_imdblookup(self, imdb_id):
        tree = self.tmdb_method('Movie.imdbLookup', imdb_id)
        movie_node = tree.find('movies')[0]
        return TheMovieDB.Movie(movie_node)

    def movie_search(self, title):
        results = []
        tree = self.tmdb_method('Movie.search', title)
        for movie_node in tree.find('movies'):
            movie = TheMovieDB.Movie(movie_node)
            if movie.name:
                results.append(movie)
        return results

if __name__ == '__main__':
    key = '825fa5f878fa024482c816d84d6431cd'
    tmdb = TheMovieDB(key)
    movie = tmdb.movie_getinfo(1832)
    print movie.name
    for c in movie.categories:
        print c.name
    for c in movie.cast:
        print c.job, c.name
    results = tmdb.movie_search('Toy+Story')
    for movie in results:
        print movie.id, '-', movie.name
