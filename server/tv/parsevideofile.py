#!/usr/bin/python

# Test out various regular expressions to match filenames fot TV episodes

from tv.models import VideoFilePattern
import re
import os


filePatterns = None

def loadPatterns():
    # Loads the patterns from the database and compiles them into memory
    global filePatterns
    filePatterns = []
    for dbpattern in VideoFilePattern.objects.all():
        newpattern={}
        newpattern['desc'] = dbpattern.description
        newpattern['re'] = re.compile(dbpattern.re)
        filePatterns.append(newpattern)

def parsevideofile(filename):
    global filePatterns
    file, ext = os.path.splitext(filename)
    for pattern in filePatterns:
        m = pattern['re'].match(file)
        if m:
            return m.groupdict()
            break
    return None

# When module is first loaded, also load the patterns
loadPatterns()
