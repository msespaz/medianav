# MediaNav code for pylirc

import pygame
import os

lirc = None

key_mapping = {
        'DOWN' : pygame.K_DOWN,
        'UP'   : pygame.K_UP,
        'LEFT' : pygame.K_LEFT,
        'RIGHT'   : pygame.K_RIGHT,
        'PGDOWN' : pygame.K_PAGEDOWN,
        'PGUP'   : pygame.K_PAGEUP,
        'SELECT' : pygame.K_RETURN,
        'BACK'   : pygame.K_BACKSPACE,
        'LIVETV'   : pygame.K_TAB,
        }


def init():
    """ Initializes pylirc """
    print "init pylirc"
    import pylirc
    lirc = pylirc.init('pyhtpc', os.getenv('HOME')+'/.lircrc', 0)

def get_events():
    """ Gets all the pylirc codes and converts them to pygame events """
    import pylirc
    events = []
    lirc_codes = pylirc.nextcode(1)
    if lirc_codes:
        for code in lirc_codes:
            if code['repeat'] == 0 or code['repeat'] > 2:
                if key_mapping.has_key(code['config']):
                    events.append(pygame.event.Event(pygame.KEYDOWN, key=key_mapping[code['config']]))
    return events
