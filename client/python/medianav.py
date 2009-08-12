#!/usr/bin/python

from components import *
from tv import TVPage, TVEpisodesPage
from pygame import Rect
from random import randrange
from utils import *
import config

def decorate_page(page):
    """ Adds stuff that is common to all pages """
    # Add a clock and FPS widget
    page.add_widget(Clock(Rect(page.screen_width-250,10, 100, 100), font_size=30))
    page.add_widget(FPS(Rect(page.screen_width-100,page.screen_height-20, 100, 100)))
    title = Title(Rect(10,10,100,100), 'MediaNav')
    page.add_widget(title)
    page.load_background(config.BACKGROUND)

class ScreenSaverClock(Page):
    """ A screensaver that displays the current date and time """
    def __init__(self, app, parent=None, color=(0, 0, 0)):
        Page.__init__(self, app, parent, color)
        self.clock = Clock(Rect(0, 0, 100,100), font_size=40)
        self.add_widget(self.clock)
        self.last_moved = 0
        self.old_x = 0
        self.old_y = 0
        self.new_x = 0
        self.new_y = 0
        self.move_random()

    def move_random(self):
        self.old_x = self.new_x
        self.old_y = self.new_y
        self.new_x = randrange(0,self.screen_width-40)+20
        self.new_y = randrange(0,self.screen_height-50)+25

    def update(self, dx):
        Page.update(self, dx)
        self.last_moved += dx
        if self.last_moved > 5000:
            self.move_random()
            self.last_moved -= 5000 
        distance = self.last_moved/5000.0
        self.clock.rect.topleft=(
                interp_log(self.old_x, self.new_x, distance),
                interp_log(self.old_y, self.new_y, distance))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.send_app_event(Event('page_back', None))

class MainPage(Page):
    """ The main page """
    def __init__(self, app, parent=None, color=(0, 0, 196)):
        Page.__init__(self, app, parent, color)

        # Create a menu in the middle of the screen
        self.main_menu = Menu(Rect(self.screen_width/4, self.screen_height/4, self.screen_width/2, self.screen_height/2),
                font_size=60)
        self.main_menu.add_item(MenuItem('Movies'))
        self.main_menu.add_item(MenuItem('TV Shows'))
        self.main_menu.add_item(MenuItem('File Browser'))
        self.main_menu.add_item(MenuItem('Screen Saver'))
        self.main_menu.select_item(0)
        self.add_widget(self.main_menu, is_event_listener=True, is_event_dispatcher=True)
    
    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'menu_select':
            self.send_app_event(Event('page_forward', event.data[1].text))

class FileBrowserPage(Page):
    """ File Browser page """
    def __init__(self, app, path, parent=None, color=(0, 0, 196)):
        Page.__init__(self, app, parent, color)
        self.title = Title(Rect(self.screen_width/2,10,100,100), 'File Browser')
        self.add_widget(self.title)
        self.path_label = Label(Rect(10, 40, 10, 10), path)
        self.add_widget(self.path_label)
        # Create a menu in the middle of the screen
        self.file_menu = FileMenu(Rect(self.screen_width/8, self.screen_height/8, self.screen_width/2, self.screen_height/1.5),
                path=path)
        self.add_widget(self.file_menu, is_event_listener=True, is_event_dispatcher=True)

    def handle_event(self, event):
        Page.handle_event(self, event)
        if event.type == 'filemenu_pathchange':
            self.path_label.set_text(event.data)
        if event.type == 'filemenu_launch':
            print "Launching file ", event.data
            play_file(event.data)

class MyApp(App):
    def __init__(self, screen_size=(1920,1080)):
        App.__init__(self, screen_size)
        self.main_page = MainPage(self)
        decorate_page(self.main_page)
        self.filebrowser_page = FileBrowserPage(self, config.FILEBROWSER_PATH)
        decorate_page(self.filebrowser_page)
        self.screensaver_page = ScreenSaverClock(self)
        
        # TV shows
        self.tv_page = TVPage(self)
        decorate_page(self.tv_page)

        self.set_page(self.main_page)

    def tick(self):
        # Implement screensaver
        if self.current_page <> self.screensaver_page:
            if self.screensaver_timer > 20000: # Hardcoded at 5 seconds for now
                self.screensaver_timer = 0
                self.page_forward(self.screensaver_page)

    def handle_page_event(self, event):
        # Page navigation for the main page
        if event.type == 'page_forward':
            if event.data == 'TV Shows':
                self.page_forward(self.tv_page)
            if event.data == 'File Browser':
                self.page_forward(self.filebrowser_page)
            if event.data == 'Movies':
                print "Page change to Movies"
            if event.data == 'Screen Saver':
                print self.screensaver_page
                print self.current_page
                self.page_forward(self.screensaver_page)
        if event.type == 'page_back':
            self.page_back()
        if event.type == 'page_tvshow':
            show = event.data
            print "Changing TV show to", show
            tv_episodes_page = TVEpisodesPage(self, show)
            decorate_page(tv_episodes_page)
            self.page_forward(tv_episodes_page)
        

if __name__ == "__main__":
    app = MyApp()
    app.run()
