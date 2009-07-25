from django.core.management.base import LabelCommand
from tv.thetvdbapi import TheTVDB
from django.conf import settings

class Command(LabelCommand):
    def handle_label(self, label, **options):
        tvdbapi = TheTVDB(settings.TVDBAPI_KEY)
        shows=tvdbapi.get_matching_shows(label)
        if shows:
            for show in shows:
                print "%s %s" % show
            print "%d show(s) found." % (len(shows))
        else:
            print "No shows matching %s found." % (label,)

