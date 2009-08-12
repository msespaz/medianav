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
SERVER = config.get('Options', 'server')

# Check if should use pylirc
LIRC = config.getboolean('Options', 'lirc')
