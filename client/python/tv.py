## Page handling TV episodes for MediaNav

from components import *
from pygame import Rect
import config
import urllib2
import StringIO

import simplejson

def get_show_list():
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + '/tv/json/shows/').read()
    json_shows = simplejson.loads(result)
    shows = []
    for json_show in json_shows:
        show = {}
        show['banner_url'] = "%s/tv/media/img/banner/%s.jpg" % (config.SERVER, json_show['fields']['tvdb_showid'])
        show['poster_url'] = "%s/tv/media/img/poster/%s.jpg" % (config.SERVER, json_show['fields']['tvdb_showid'])
        show['fanart_url'] = "%s/tv/media/img/fanart/%s.jpg" % (config.SERVER, json_show['fields']['tvdb_showid'])
        show['name'] = json_show['fields']['name']
        show['pk'] = json_show['pk']
        shows.append(show)
    return shows

def get_episode_list(show_id):
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + "/tv/json/show/%d/episodes/" % show_id).read()
    json_episodes = simplejson.loads(result)
    episodes = []
    for json_episode in json_episodes:
        episode = {}
        episode['image_url'] = "http://www.thetvdb.com/banners/_cache/%s" % json_episode['fields']['tvdb_image']
        episode['overview'] = json_episode['fields']['overview']
        episode['episode_number'] = json_episode['fields']['episode_number']
        episode['season_number'] = json_episode['fields']['season_number']
        episode['first_aired'] = json_episode['fields']['first_aired']
        episode['name'] = json_episode['fields']['name']
        episode['pk'] = json_episode['pk']
        episodes.append(episode)
    return episodes

def get_videofile_list(episode_id):
    base_url = config.SERVER
    result = urllib2.urlopen(base_url + "/tv/json/episode/%d/videofiles/" % episode_id).read()
    json_result = simplejson.loads(result)
    result = []
    for entry in json_result:
        item = {}
        item['name'] = entry['fields']['name']
        item['pk'] = entry['pk']
        result.append(item)
    return result

class TVPage(Page):
    def __init__(self, app, parent=None, color=(0, 0, 0)):
        Page.__init__(self, app, parent, color)
        self.title = Title(Rect(self.screen_width/2,10,100,100), 'TV Shows')
        self.add_widget(self.title)
        self.show_menu = Menu(Rect(self.screen_width/8, self.screen_height/8, self.screen_width/2, self.screen_height/1.5), font_size=37)
        self.add_widget(self.show_menu, is_event_listener=True, is_event_dispatcher=True)

        self.load_shows()

    def load_shows(self):
        """ Loads a list of shows into the menu """
        for show in get_show_list():
            self.show_menu.add_item(MenuItem(show['name'], show))
        self.show_menu.select_item(0)

    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'menu_select':
            self.send_app_event(Event('page_tvshow', event.data[1].data))
        if event.type == 'menu_hover':
            print "Update through hover"
            item = event.data[1]
            show = item.data
            print show['poster_url']
            # Try to update the background
            try:
                fanart = StringIO.StringIO(urllib2.urlopen(show['fanart_url']).read())
                self.load_background(fanart)
            except:
                self.load_background(config.BACKGROUND)

class TVEpisodesPage(Page):
    """ Shows a list of episodes for TV Show """
    def __init__(self, app, show, parent=None, color=(0, 0, 0)):
        Page.__init__(self, app, parent, color)
        self.show = show
        self.title = Title(Rect(self.screen_width/2,10,100,100), 'TV Shows - %s' % show['name'])
        self.add_widget(self.title)

        # Hardcoded positions for 1280x1090
        self.episode_menu = Menu(Rect(40, 275, 1100, 510), font_size=40)
        self.add_widget(self.episode_menu, is_event_listener=True, is_event_dispatcher=True)

        self.load_episodes()
        self.episode_image = ImageWidget(Rect(740, 820, 400, 220))
        self.add_widget(self.episode_image)
        self.banner_image = ImageWidget(Rect(40, 95, 758, 140))
        self.banner_image.load_image_url(self.show['banner_url'])
        self.add_widget(self.banner_image)
        self.poster_image = ImageWidget(Rect(1200, 40, 680, 1000))
        self.poster_image.load_image_url(self.show['poster_url'])
        self.add_widget(self.poster_image)
        self.infoblock = TextBlock(Rect(40, 820, 665, 220), 'Information block', font_size=30)
        self.add_widget(self.infoblock)

    def load_background(self, filename):
        """ Overrides the default background behaviour """
        # Try to update the background
        try:
            print "Trying to load background"
            background = StringIO.StringIO(urllib2.urlopen(self.show['fanart_url']).read())
            Page.load_background(self, background)
            print "Loaded background"
        except:
            print "Failed to load background"
            Page.load_background(self, config.BACKGROUND)

    def load_episodes(self):
        """ Loads a list of shows into the menu """
        for episode in get_episode_list(self.show['pk']):
            self.episode_menu.add_item(MenuItem(
                "%d x %d : %s " % (
                    episode['season_number'],
                    episode['episode_number'],
                    episode['name'],
                    ), 
                episode))
        self.episode_menu.select_item(0)

    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'menu_select':
            item = event.data[1]
            episode = item.data
            videofiles = get_videofile_list(episode['pk'])
            for videofile in videofiles:
                filename = os.path.join(config.TV_PATH, videofile['name'])
                print "Launching file ", filename
                play_file(filename)
        if event.type == 'menu_hover':
            item = event.data[1]
            episode = item.data
            self.infoblock.set_text('%s | %s ' % (episode['first_aired'], episode['overview']))
            # Try to update the episode image
            #try:
            #    episode_image = StringIO.StringIO(urllib2.urlopen(episode['image_url']).read())
            #    self.episode_image.load_image(episode_image)
            #except:
            #    self.episode_image.clear_image()
