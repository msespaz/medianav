from django.core.management.base import LabelCommand
from tv.models import *
from django.contrib.auth.models import User
from django.conf import settings
import os

SOURCEPATH=settings.MEDIANAV_TV_DIR
TARGETPATH=settings.MEDIANAV_TV_COPY_DIR

class Command(LabelCommand):
    def handle_label(self, label, **options):
        username=label
        user = User.objects.get(username=username)
        fav_shows = user.show_set.all()
        unseen_list = []
        for show in fav_shows:
            episodes = show.episode_set.filter(videofile__isnull=False).exclude(seen_by=user)
            for episode in episodes:
                videopath = episode.videofile_set.all()[0].name
                videodir, videofile = os.path.split(videopath)
                targetdirectory = os.path.join(TARGETPATH, username, videodir)
                targetfile = os.path.join(TARGETPATH, username, videopath)
                sourcefile = os.path.join(SOURCEPATH, videopath)
                try:
                    os.makedirs(targetdirectory)
                except:
                    pass
                print sourcefile, targetfile
                if os.path.isfile(sourcefile):
                    user.episode_set.add(episode)
                    try:
                        os.symlink(sourcefile, targetfile)
                    except:
                        pass

