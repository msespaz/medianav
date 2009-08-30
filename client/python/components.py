
# Part of MediaNav client
# Defines the component objects

import pygame
import sys
import os
import math
from utils import *
import time
from eventmanager import Event, EventManager
import lirc
import urllib2
import StringIO

class MediaNavNode(object):
    """ Base object from which all MediaNav objects are derived """
    def __init__(self):
        self.is_event_listener = False #: Does this node listen for events?
        self.is_event_dispatcher = False #: Does this node send events?
        self.event_manager = None

    def set_event_manager(self, event_manager):
        """ For the node to be able to send or receive events it must
            have an event manager """
        self.event_manager = event_manager
    
    def handle_event(self, event):
        """ If the node is an event listener this will be called when an
            event is received """
        #print self.__class__, event # DEBUG
        pass

    def dispatch_event(self, event):
        """ Dispatches an event via the event manager """
        if self.event_manager:
            self.event_manager.dispatch_event(event)

class Widget(MediaNavNode):
    """ The base widget class from which the other types inherit """
    def __init__(self, rect):
        """ Init the widget using a rect to define size and position """
        MediaNavNode.__init__(self)
        if not isinstance(rect, pygame.Rect):
            raise Exception, "Widget rect not a pygame.Rect object"
        self.rect = rect #: This is a pygame.Rect object
        self.dirty = True #: Indicates if the widget is dirty and should be redrawn

    def draw(self, surface):
        """ This method should be overidden. Each widget should be able to
            draw itself to a target surface.
        """
        pass

    def update(self, dx):
        """ Used for animation and updates in the widget
            dx should be the time between the last time this was called.
            Typically this is the return value from pygame.time.Clock.tick()
        """
        pass


class Page(MediaNavNode):
    """ A container for something that is displayed on the screen """
    def __init__(self, app, parent=None, background_color=(0,0,0)):
        MediaNavNode.__init__(self)
        self.screen = app.screen #: The screen surface to draw to
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.background_color = background_color #: The background color to fill the screen with
        self.background_image = None
        self.parent = parent #: The parent page, used for navigation
        self.widgets = [] #: A list of widgets in this page
        self.app = app #: The app object under which this page runs

        # Load the background
        # TODO: Remove hardcoding of background

        # Make the page an event dispatcher
        self.set_event_manager(EventManager())
        self.is_event_dispatcher = True

        # Make the page an event listener
        self.event_manager.register_listener(self)
        self.is_event_listener=True

    def set_parent(self, parent):
        """ Sets the parent page, used for page navigation """
        self.parent = parent

    def load_background(self, filename):
        image = pygame.image.load(filename)
        self.background_image = pygame.transform.smoothscale(image, (self.screen_width, self.screen_height)).convert()

    def add_widget(self, widget, is_event_listener=False, is_event_dispatcher=False):
        """ Add a widget to the page """
        if is_event_listener == True:
            # If this widget will listen to events, make it a listener
            self.event_manager.register_listener(widget)
            widget.is_event_listener = True
        if is_event_dispatcher == True:
            # If this widget will send events set the event manager
            widget.set_event_manager(self.event_manager)
            widget.is_event_dispatcher = True

        self.widgets.append(widget)

    def handle_pygame_event(self, event):
        """ Events that come from pygame should be dispatched to all listeners """
        self.event_manager.dispatch_event(event)

    def handle_event(self, event):
        """ Handle events generated by widgets 
            By default this only handles page back events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.send_app_event(Event('page_back', None))


    def send_app_event(self, event):
        """ Sends an event to the app object """
        self.app.handle_page_event(event)

    def draw(self):
        """ Draws the page on the screen """
        # Clear the surface
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.background_color)
        # Draw all the widgets
        for widget in self.widgets:
        #    if widget.dirty:
             widget.draw(self.screen)

    def update(self, dx):
        """ Used for animation and updates
            dx should be the time between the last call
            Typically this is the return value from pygame.time.Clock.tick()
        """
        # Update the widgets
        for widget in self.widgets:
            widget.update(dx)

class Label(Widget):
    """ A text label widget """
    def __init__(self, rect, text='Label', font_size=40, font_color=(255, 255, 255)):
        Widget.__init__(self, rect)
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.font_color = font_color
        self.rendered_label = None
        self.render_label()

    def set_text(self, text):
        self.text = text
        self.render_label()
    
    def render_label(self):
        """ This re-renders the text to a bitmap that can be blitted later """
        self.rendered_label = self.font.render(self.text, True, self.font_color)
    
    def draw(self, surface):
        surface.blit(self.rendered_label, self.rect)

class TextBlock(Widget):
    """ Text constrained to a rect with wrapping """
    def __init__(self, rect, text='Label', font_size=30, font_color=(255, 255, 255), background_color=(0, 0, 0, 128)):
        Widget.__init__(self, rect)
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.font_color = font_color
        self.background_color = background_color
        self.text_surface = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.render_text()

    def set_text(self, text):
        self.text = text
        self.render_text()

    def render_text(self):
        """ Renders the text to internal surface for blitting later """
        self.text_surface.fill (self.background_color)
        # Split up input into lines
        outputlines = []
        newline = ''
        for word in self.text.split(' '):
            templine = newline + word + " "
            if self.font.size(templine)[0] < self.rect.width:
                newline = templine
            else:
                outputlines.append(newline)
                newline = word + " "

        # Render the lines
        y_offset = 0
        for line in outputlines:
            self.text_surface.blit(self.font.render(line, True, self.font_color), (0, y_offset))
            y_offset += self.font.get_linesize()

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)

class Clock(Label):
    """ A widget that displays the current date/time """
    def __init__(self, rect, format="%a %y/%m/%d %H:%M:%S", font_size=20, upd_interval=1000):
        Label.__init__(self, rect, font_size=font_size)
        self.format = format #: The time.strftime string format
        self.upd_interval = upd_interval #: The number of milliseconds between updates
        self.last_updated = 0 #: Number of milliseconds since last update
        self.update_time()

    def update_time(self):
        self.text = time.strftime(self.format)
        self.render_label()

    def update(self, dx):
        self.last_updated += dx
        if self.last_updated > self.upd_interval:
            self.update_time()
            self.last_updated = 0

    def draw(self, surface):
        Label.draw(self, surface)

class FPS(Label):
    """ A widget that displays the framerate """
    def __init__(self, rect, font_size=20, upd_interval=1000):
        Label.__init__(self, rect, font_size=font_size, text='FPS: ?')
        self.upd_interval = upd_interval #: The number of milliseconds between updates
        self.last_updated = 0 #: Number of milliseconds since last update
        self.frames = 0 #: The number of frames per update

    def update(self, dx):
        self.last_updated += dx
        self.frames += 1
        if self.last_updated > self.upd_interval:
            self.text = "FPS: %f" % (1000.0 * self.frames / self.last_updated)
            self.render_label()
            self.last_updated = 0
            self.frames = 0

    def draw(self, surface):
        Label.draw(self, surface)

class Title(Label):
    """ A title for a page. This is a special type of label that centers itself """
    def __init__(self, rect, title_text):
        # TODO: Center the label
        Label.__init__(self, rect, title_text)

class Box(Widget):
    """ A widget that draws a filled rectangle """
    def __init__(self, rect, color):
        Widget.__init__(self, rect)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ImageWidget(Widget):
    """ An image widget """
    def __init__(self, rect, image_name=None, color=(0, 0, 0, 128)):
        Widget.__init__(self, rect)
        self.color = color
        self.image_name = image_name
        if self.image_name:
            self.load_image(self.image_name)
        else:
            self.clear_image()

    def load_image(self, image_name):
        image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(image, (self.rect.width, self.rect.height)).convert()

    def load_image_url(self, url):
        try:
            fileobj=StringIO.StringIO(urllib2.urlopen(url).read())
            self.load_image(fileobj)
        except:
            self.clear_image()

    def clear_image(self):
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.image.fill (self.color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class MenuItem:
    def __init__(self, text, data=None):
        self.text = text
        self.data = data

class Menu(Widget):
    """ A menu """
    def __init__(self, rect, selected_item_number=0, font_size=40, default_color=(196,196,196), selected_color=(128,255,255), background_color=(0, 0, 0, 128)):
        Widget.__init__(self, rect)

        self.items = [] 
        self.selected_item_number = selected_item_number 
        self.font = pygame.font.SysFont("arial", font_size)
        
        self.default_color = default_color
        self.selected_color = selected_color
        self.background_color = background_color

        # Create a surface for the menu
        self.menu_surface = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        # self.menu_surface = pygame.Surface((self.width, self.height))

        # The menu needs to handle events for navigation
        self.is_event_handler = True

        self.font_size = self.font.get_linesize()
        self.top_item = 0 #: The item that is currently top in the view
        self.items_per_page = self.rect.height // self.font_size

        self.select_item(0)

        self.hover_time_count = 0 #: How long the selection has been hovering over the current item
        self.hover_time = 500 #: How long to wait before sending a hover event_
        self.hover_sent = False

    def handle_event(self, event):
        """ Handles pygame events for navigation """
        Widget.handle_event(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_item(self.selected_item_number-1)
            if event.key == pygame.K_DOWN:
                self.select_item(self.selected_item_number+1)
            if event.key == pygame.K_PAGEUP:
                self.select_item(self.selected_item_number-(self.items_per_page-1))
            if event.key == pygame.K_PAGEDOWN:
                self.select_item(self.selected_item_number+(self.items_per_page-1))
            if event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT:
                self.dispatch_event(Event('menu_select', (self.selected_item_number, self.items[self.selected_item_number])))

    def update(self, dx):
        """ For hover events """
        if not self.hover_sent:
            self.hover_time_count += dx
            if self.hover_time_count > self.hover_time:
                self.hover_time_count = 0
                self.dispatch_event(Event('menu_hover', (self.selected_item_number, self.items[self.selected_item_number])))
                self.hover_sent = True

    def render_surface(self):
        """ Renders menu to surface """
        self.menu_surface.fill (self.background_color)
        # Draw only the items that will fit in the screen, plus 1 in case one is cropped
        for index in range(self.top_item, self.top_item + self.items_per_page + 1):
            if index >= len(self.items):
                break
            if index == self.selected_item_number:
                font_color = self.selected_color
            else:
                font_color = self.default_color
            item = self.items[index]
            # Render text onto the surface 
            self.menu_surface.blit(self.font.render(item.text, True, font_color), (0, self.font_size * (index-self.top_item)))

    def select_item(self, item_number):
        # See if we are moving up, or down
        if item_number < self.selected_item_number:
            direction='up'
        else:
            direction='down'

        # Reset hover trigger
        if self.selected_item_number <> item_number:
            self.hover_sent = False
            self.hover_time_count = 0

        # Selects a particular item
        self.selected_item_number = item_number

        # Prevent selection of items not in the list
        if self.selected_item_number < 0:
            self.selected_item_number = 0
        if self.selected_item_number >= len(self.items):
            self.selected_item_number = len(self.items) - 1

        # Adjust the top item in the list to ensure the selected item is visible
        if direction == 'down':
            while self.selected_item_number > self.top_item + self.items_per_page - 1:
                self.top_item += 1
        if direction == 'up': 
            while self.selected_item_number < self.top_item:
                self.top_item -= 1

        self.render_surface()
        self.dirty = True

    def add_item(self, item):
        self.items.append(item)

    def clear_items(self):
        self.items = []

    def draw(self, surface):
        # The menu_surface contains the whole rendered menu
        # this will blit the visible portion of that onto the screen
        surface.blit(self.menu_surface, self.rect)
        self.dirty = False

class FileMenu(Menu):
    """ A file browser menu """
    def __init__(self, rect, path, selected_item_number=0, font_size=40, default_color=(196,196,196), selected_color=(128,255,255), background_color=(0, 0, 0, 128)):
        Menu.__init__(self, rect, selected_item_number=selected_item_number, font_size=font_size, default_color=default_color, selected_color=selected_color, background_color=background_color)
        self.path = path
        self.selected_stack = []
        self.update_path(path)

    def update_path(self, path, forward=True):
        self.clear_items()
        self.path = os.path.abspath(path)
        for filename in sorted(os.listdir(self.path)):
            self.add_item(MenuItem(filename))
        if forward: #: If we are going down a directory
            # Store our current position in a list
            self.selected_stack.append(self.selected_item_number)
            # Select the top item of the new directory
            self.select_item(0)
        else: #: We are going up a directory
            # If there is an item number on the stack, retrieve it
            if len(self.selected_stack):
                self.select_item(self.selected_stack.pop())
            else:
                self.select_item(0)

        self.dispatch_event(Event('filemenu_pathchange', self.path))

    def handle_event(self, event):
        """ Handles pygame events for navigation """
        Menu.handle_event(self, event)
        if event.type == 'menu_select':
            if os.path.isdir(os.path.join(self.path, event.data[1].text)):
                self.update_path(os.path.join(self.path, event.data[1].text))
            else:
                self.dispatch_event(Event('filemenu_launch', os.path.join(self.path, event.data[1].text)))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Try and go one directory up
                self.update_path(os.path.join(self.path, '..'), False)

class App(object):
    """ The main application class """
    def __init__(self, screen_size=(1280,720), framerate=30):
        pygame.init()
        if config.LIRC:
            lirc.init()
        #self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
        pygame.mouse.set_visible(0)
        #self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_page = None
        self.framerate = framerate
        self.tick_counter = 0
        self.tick_interval = 1000 #: Interval at which to call self.tick()

        # Screensaver counters
        self.screensaver_timer = 0

    def set_page(self, page):
        """ Sets a page without changing its parent """
        self.current_page = page

    def page_forward(self, page):
        """ Moves forward to a page, storing the current page as parent """
        page.set_parent(self.current_page)
        self.current_page = page
    
    def page_back(self):
        """ Moves back to the parent page, if set """
        if self.current_page.parent:
            self.current_page=self.current_page.parent

    def handle_page_event(self, event):
        """ Handles an event from a page """
        pass

    def tick(self):
        """ This is called roughly every self.tick_interval milliseconds
            You can attach something to this that needs to be called
            periodically """
        pass

    def run(self):
        """ Runs the main loop of the application """
        while self.running:
            # Limit framerate
            dx = self.clock.tick(self.framerate)
            #dx = self.clock.tick()
            # Call tick
            self.tick_counter += dx
            if self.tick_counter > self.tick_interval:
                self.tick_counter -= self.tick_interval
                self.tick()
            # Screensaver
            self.screensaver_timer += dx
            # Process events
            pygame_events = pygame.event.get() # Get pygame events
            if config.LIRC:
                lirc_codes = lirc.get_events() # Get lirc events
                events = pygame_events + lirc_codes
            else:
                events = pygame_events
            for event in events:
                if self.current_page:
                    self.current_page.handle_pygame_event(event)
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    self.screensaver_timer = 0 # For screensaver support
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return
            # Update and draw current page
            if self.current_page:
                self.current_page.update(dx)
                self.current_page.draw()
            # Draw it to the screen
            pygame.display.flip()

