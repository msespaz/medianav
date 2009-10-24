#!/usr/bin/python

# Scans directories for TV episodes

import os
from tv.parsevideofile import parsevideofile
from django.core.management.base import LabelCommand
from tv.models import Show, Episode, TVVideoFile, AlternateShowName
from django.conf import settings

class Command(LabelCommand):
    def handle_label(self, label, **options):
        verbose = False
        filename = label
        name = filename.replace(settings.MEDIANAV_TV_DIR,'',1)
        name = name.lstrip(os.sep)
        parsed=parsevideofile(name)
        if parsed is None:
            print "Cannot parse file %s" % (name,)
            return
        if 'name' not in parsed:
            print "Cannot parse show name from %s" % (name,)
            return
        # Try to match it to a show, if we have a match we can add
        # it to the database
        try:
            show = Show.objects.get(name__iexact=parsed['name'])
        except Show.DoesNotExist:
            # Try to find the show from the alternate names 
            try:
                show = AlternateShowName.objects.get(name__iexact=parsed['name']).show
            except AlternateShowName.DoesNotExist:
                print "Cannot match Show %s" % (parsed['name'],)
                return 
        # Check if this file is already in the database
        try:
            videofile = TVVideoFile.objects.get(name__iexact=name)
            if verbose: print "Updating %s" % (name,)
            videofile.name=name # Update name in case case changed
            videofile.show=show # Update show it relates to
        except TVVideoFile.DoesNotExist:
            if verbose: print "Creating %s" % (name,)
            videofile = TVVideoFile(name=name, show=show)
            videofile.save() # Must save it before we can add many-to-many later
        # Update mediainfo for videofile
        if videofile.update_mediainfo():
            print "    Updated mediainfo", videofile.name, videofile.format_name()
        # Try to match it to an episode
        # We can only do this is both season and episode numbers exist
        if ('season' in parsed) and (parsed['season'] is not None) and ('episode' in parsed) and (parsed['episode'] is not None):
            startep_number = int(parsed['episode'])
            season_number = int(parsed['season'])

            # Check if it covers more than one episode
            if ('endep' in parsed) and (parsed['endep'] is not None):
                endep_number = int(parsed['endep'])
            else:
                endep_number = startep_number
            # Sanity check to make sure the endep is valid
            if endep_number < startep_number:
                endep_number = startep_number
            # Loop through the episodes and add them if we find them
            for ep_number in range(startep_number, endep_number+1):
                # Because of data inconsistencies in TheTVDB's data there might be
                # duplicates. Assign this to all occurrences of the episode in the DB
                # FIXME This should be picked up during a consistency check and
                # reported to TheTVDB to clean up
                episodes = Episode.objects.filter(show=show, season_number=season_number, episode_number = ep_number)
                for episode in episodes:
                    print "    Linking episode ", episode
                    videofile.episodes.add(episode)

        videofile.save()



