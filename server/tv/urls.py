from django.conf.urls.defaults import *
from django.views import static

from django_restapi.model_resource import Collection
from django_restapi.responder import JSONResponder

from tv.models import Show
from tv.models import Episode
from tv.models import VideoFile

# Creates a custom collection filtered by show
# Based on the example from
# http://django-rest-interface.googlecode.com/svn/trunk/django_restapi_tests/examples/custom_urls.py
class EpisodeCollection(Collection):
    # Returns all the episodes, called when is_entry is False
    def read(self, request):
        show_id = int(request.path.split("/")[4])
        filtered_set = self.queryset._clone()
        filtered_set = filtered_set.filter(show__id=show_id,videofile__isnull = False)
        return self.responder.list(request, filtered_set)

json_show_resource = Collection(
        queryset = Show.objects.all(),
        responder = JSONResponder()
)

json_episode_resource = EpisodeCollection(
        queryset = Episode.objects.all(),
        responder = JSONResponder()
)

class VideoFileCollection(Collection):
    # Returns all the videofiles, called when is_entry is False
    def read(self, request):
        episode_id = int(request.path.split("/")[4])
        filtered_set = self.queryset._clone()
        filtered_set = filtered_set.filter(episodes__id=episode_id)
        return self.responder.list(request, filtered_set)

json_videofile_resource = VideoFileCollection(
        queryset = VideoFile.objects.all(),
        responder = JSONResponder()
)

urlpatterns = patterns('tv.views',
    (r'^$', 'shows_list'),
    (r'^show/(?P<show_id>\d+)/$', 'show_detail'),
    (r'^episode/(?P<episode_id>\d+)/$', 'episode_detail'),
    (r'^missing/$', 'missing_episodes'),
    (r'^media/(?P<path>.*)$', static.serve, {'document_root': 'tv/media', 'show_indexes': True}),
    (r'^json/show/(?P<show_id>\d+)/episodes/$', json_episode_resource, {'is_entry':False}),
    (r'^json/episode/(\d+)/?$', json_episode_resource, {'is_entry':True}),
    (r'^json/episode/(?P<episode_id>\d+)/videofiles/$', json_videofile_resource, {'is_entry':False}),
    (r'^json/videofile/(\d+)/?$', json_videofile_resource, {'is_entry':True}),
    (r'^json/show/(.*?)/?$', json_show_resource),
)
