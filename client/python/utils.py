
# Part of MediaNav client
# Defines some utility functions

import math
import os
import config

def interp_lin(value1, value2, factor):
    """ Interpolates between two values linearly
        The return value will be:
          value1 if factor is 0 
          value2 if factor is 1
    """
    return value1+(value2-value1)*factor

def interp_log(value1, value2, factor):
    """ Interpolates between two values logarithmically
        The return value will be:
          value1 if factor is 0 
          value2 if factor is 1
    """
    log_factor = math.log(interp_lin(1, 10, factor), 10)
    return interp_lin(value1, value2, log_factor)

def play_file(file):
    """ Plays a video file, file is the full path and filename """
    cmd = config.PLAYER_CMD % (file)
    os.system(cmd)
