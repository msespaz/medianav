## Page handling Movies for MediaNav

from components import *
from pygame import Rect
import config
import urllib2
import StringIO

import simplejson

def get_genre_list():
    base_url = config.SERVER
    html = urllib2.urlopen(base_url + 'movies/json/genres/').read()
    json = simplejson.loads(html)
    genres = {}
    for j in json:
        genres[j['pk']] = j['fields']['name']
    return genres

def get_movie_list():
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + 'movies/json/movies/').read()
    json_movies = simplejson.loads(result)
    movies = []
    for json_movie in json_movies:
        movie = {}
        movie['poster_url'] = "%smedia/img/movies/poster/%s.jpg" % (config.SERVER, json_movie['fields']['moviedb_id'])
        movie['backdrop_url'] = "%smedia/img/movies/backdrop/%s.jpg" % (config.SERVER, json_movie['fields']['moviedb_id'])
        movie['title'] = json_movie['fields']['title']
        movie['year'] = json_movie['fields']['year']
        movie['genres'] = json_movie['fields']['genres']
        movie['pk'] = json_movie['pk']
        movies.append(movie)
    return movies

def get_movie_detail(movie_id):
    base_url = config.SERVER
    html = urllib2.urlopen(base_url + 'movies/json/movie/%s/' % movie_id).read()
    json = simplejson.loads(html)
    movie = json[0]['fields']
    movie['pk'] = movie_id
    movie['poster_url'] = "%smedia/img/movies/poster/%s.jpg" % (config.SERVER, movie['moviedb_id'])
    movie['backdrop_url'] = "%smedia/img/movies/backdrop/%s.jpg" % (config.SERVER, movie['moviedb_id'])
    return movie

def get_directory_list(movie_id):
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + "movies/json/movie/%d/directories/" % movie_id).read()
    json_directories = simplejson.loads(result)
    directories = []
    for json_directory in json_directories:
        directory = {}
        directory['name'] = json_directory['fields']['name']
        directory['pk'] = json_directory['pk']
        directories.append(directory)
    return directories

def get_videofile_list(directory_id):
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + "movies/json/directory/%d/videofiles/" % directory_id).read()
    json_result = simplejson.loads(result)
    result = []
    for entry in json_result:
        item = {}
        item['name'] = entry['fields']['name']
        item['pk'] = entry['pk']
        result.append(item)
    return result

class MoviesPage(Page):
    def __init__(self, app, parent=None, color=(0, 0, 0)):
        Page.__init__(self, app, parent, color)
        self.title = Title(Rect(self.screen_width/2,10,100,100), 'Movies')
        self.add_widget(self.title)
        self.movie_menu = Menu(Rect(self.screen_width/8, self.screen_height/8, self.screen_width/2, self.screen_height/1.5), font_size=37)
        self.add_widget(self.movie_menu, is_event_listener=True, is_event_dispatcher=True)

        self.genres = get_genre_list()
        self.load_movies()

    def load_movies(self):
        """ Loads a list of movies into the menu """
        for movie in get_movie_list():
            menu_title = '%s (%s)' % (movie['title'], movie['year'])
            for g in movie['genres']:
                menu_title += ' %s' % self.genres[g]
            self.movie_menu.add_item(MenuItem(menu_title, movie))
        self.movie_menu.select_item(0)

    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'menu_select':
            self.send_app_event(Event('page_movie', event.data[1].data))
        if event.type == 'menu_hover':
            print "Update through hover"
            item = event.data[1]
            movie = item.data
            print movie['poster_url']
            # Try to update the background
            try:
                fanart = StringIO.StringIO(urllib2.urlopen(movie['backdrop_url']).read())
                self.load_background(fanart)
            except:
                self.load_background(config.BACKGROUND)

class MovieDetailPage(Page):
    """ Shows a list of directories for Movie """
    def __init__(self, app, movie, parent=None, color=(0, 0, 0)):
        Page.__init__(self, app, parent, color)
        self.movie = get_movie_detail(movie['pk'])
        self.title = Title(Rect(self.screen_width/2,10,100,100), 'Movies - %s' % self.movie['title'])
        self.add_widget(self.title)

        # Hardcoded positions for 1920x1080
        self.directory_menu = Menu(Rect(40, 275, 1100, 510), font_size=40)
        self.add_widget(self.directory_menu, is_event_listener=True, is_event_dispatcher=True)

        self.load_directories()
        self.poster_image = ImageWidget(Rect(1200, 40, 680, 1000))
        self.poster_image.load_image_url(self.movie['poster_url'])
        self.add_widget(self.poster_image)
        self.infoblock = TextBlock(Rect(40, 820, 665, 220), self.movie['plot_outline'], font_size=30)
        self.add_widget(self.infoblock)

    def load_background(self, filename):
        """ Overrides the default background behaviour """
        # Try to update the background
        try:
            print "Trying to load background"
            background = StringIO.StringIO(urllib2.urlopen(self.movie['backdrop_url']).read())
            Page.load_background(self, background)
            print "Loaded background"
        except:
            print "Failed to load background"
            Page.load_background(self, config.BACKGROUND)

    def load_directories(self):
        """ Loads a list of movies into the menu """
        for directory in get_directory_list(self.movie['pk']):
            self.directory_menu.add_item(MenuItem(
                "%s" % (
                    directory['name'],
                    ), 
                directory))
        self.directory_menu.select_item(0)

    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'menu_select':
            item = event.data[1]
            directory = item.data
            videofiles = get_videofile_list(directory['pk'])
            for videofile in videofiles:
                filename = os.path.join(config.MOVIE_PATH, directory['name'], videofile['name'])
                print "Launching file ", filename
                play_file(filename)
        if event.type == 'menu_hover':
            item = event.data[1]
            directory = item.data
            #self.infoblock.set_text('%s | %s ' % (directory['first_aired'], directory['overview']))
