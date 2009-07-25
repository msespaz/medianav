from django.core.management.base import LabelCommand
from django.conf import settings
from tv.thetvdbapi import TheTVDB
from tv.models import Show, Episode
import urllib
import os

class Command(LabelCommand):
    def handle_label(self, label, **options):
        print "Querying TheTVDB..."
        tvdbapi = TheTVDB(settings.TVDBAPI_KEY)
        show_id = label
        result = tvdbapi.get_show_and_episodes(show_id)
        if result:
            tvdbshow, tvdbepisodes = result
            print "Show.name = %s" % (tvdbshow.name,) 
            try:
                show = Show.objects.get(tvdb_showid=tvdbshow.id)
                print "Updating existing show"
            except Show.DoesNotExist:
                print "Creating new show"
                show = Show(tvdb_showid=tvdbshow.id)
            show.name = tvdbshow.name
            show.overview = tvdbshow.overview
            show.genre = str(tvdbshow.genre[0]) # FIXME This is an array
            show.network = tvdbshow.network
            show.content_rating = tvdbshow.content_rating
            show.runtime = tvdbshow.runtime
            show.status = tvdbshow.status
            show.first_aired = tvdbshow.first_aired
            show.airs_day = tvdbshow.airs_day
            show.airs_time = tvdbshow.airs_time
            show.tvdb_language = tvdbshow.language
            if tvdbshow.rating:
                show.tvdb_rating = tvdbshow.rating
            show.tvdb_banner_url = tvdbshow.banner_url
            show.tvdb_fanart_url = tvdbshow.fanart_url
            show.tvdb_poster_url = tvdbshow.poster_url
            show.tvdb_last_updated = tvdbshow.last_updated
            show.save()
            # Download the images for the show
            filename = "%s/img/banner/%d.jpg" % (settings.MEDIANAV_TV_MEDIA, show.tvdb_showid)
            if not os.access(filename, os.F_OK):
                print "Downloading banner image"
                urllib.urlretrieve(show.tvdb_banner_url, filename)
            filename = "%s/img/poster/%d.jpg" % (settings.MEDIANAV_TV_MEDIA, show.tvdb_showid)
            if not os.access(filename, os.F_OK):
                print "Downloading poster image"
                urllib.urlretrieve(show.tvdb_poster_url, filename)
            filename = "%s/img/fanart/%d.jpg" % (settings.MEDIANAV_TV_MEDIA, show.tvdb_showid)
            if not os.access(filename, os.F_OK):
                print "Downloading fanart image"
                urllib.urlretrieve(show.tvdb_fanart_url, filename)
            # Add / Update episodes from tvdb to medianav 
            for tvdbepisode in tvdbepisodes:
                update = 0
                update_fields = ""
                try:
                    print "Update: s%02de%02d %s" % (int(tvdbepisode.season_number), int(tvdbepisode.episode_number), tvdbepisode.name)
                    episode = Episode.objects.get(tvdb_episodeid=tvdbepisode.id)
                except Episode.DoesNotExist:
                    episode = Episode(tvdb_episodeid=tvdbepisode.id)
                    print "Create: s%02de%02d %s" % (int(tvdbepisode.season_number), int(tvdbepisode.episode_number), tvdbepisode.name)
                if episode.show != show:
                    episode.show = show
                    update = 1
                    update_fields += " show"
                if episode.name != tvdbepisode.name:
                    episode.name = tvdbepisode.name
                    update = 1
                    update_fields += " name"
                episode.overview = tvdbepisode.overview
                episode.season_number = tvdbepisode.season_number
                episode.episode_number = tvdbepisode.episode_number
                episode.director = tvdbepisode.director
                episode.guest_stars = tvdbepisode.guest_stars
                episode.production_code = tvdbepisode.production_code
                episode.writer = tvdbepisode.writer
                episode.first_aired = tvdbepisode.first_aired
                episode.tvdb_language = tvdbepisode.language
                if tvdbepisode.rating:
                    episode.tvdb_rating = tvdbepisode.rating
                episode.tvdb_image = tvdbepisode.image
                episode.tvdb_last_updated = tvdbepisode.last_updated
                episode.save()
                if update:
                    print "Update: s%02de%02d %s [%s]" % (int(tvdbepisode.season_number), int(tvdbepisode.episode_number), tvdbepisode.name, update_fields),
            # Remove any episodes that are no longer in tvdb list
            for episode in show.episode_set.all():
                if episode.tvdb_episodeid not in (int(e.id) for e in tvdbepisodes):
                    print "Delete: s%02de%02d %s" % (episode.season_number, episode.episode_number, episode.name)
                    episode.delete()
        else:
            print "Unable to retrieve information for show_id = %s" % (show_id,)
        
