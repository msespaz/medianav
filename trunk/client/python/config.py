# Part of MediaNav
# Defines configuration settings

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('medianav.cfg')

PLAYER_CMD = config.get('Commands', 'mplayer')
WIDTH = config.getint('Display', 'width')
HEIGHT = config.getint('Display', 'height')
FILEBROWSER_PATH = config.get('Directories', 'filebrowser')
BACKGROUND = config.get('Display', 'background')
TV_PATH = config.get('Directories', 'tv')
MOVIE_PATH = config.get('Directories', 'movies')
SERVER = config.get('Options', 'server')
USERLIST = config.get('Options', 'userlist').split(',')

user_index = 0
USER = USERLIST[user_index]

# Check if should use pylirc
LIRC = config.getboolean('Options', 'lirc')

def cycle_user():
    global user_index
    global USERLIST
    global USER
    user_index += 1
    if user_index > len(USERLIST)-1:
        user_index = 0
    USER = USERLIST[user_index]
    return USER
