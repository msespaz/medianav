from django.conf.urls.defaults import *
from django.views import static

urlpatterns = patterns('tv.views',
    (r'^$', 'shows_list'),
    (r'^show/(?P<show_id>\d+)/$', 'show_detail'),
    (r'^episode/(?P<episode_id>\d+)/$', 'episode_detail'),
    (r'^missing/$', 'missing_episodes'),
    (r'^media/(?P<path>.*)$', static.serve, {'document_root': 'tv/media', 'show_indexes': True}),
    (r'^json/shows/$', 'json_shows_list'),
    (r'^json/show/(?P<show_id>\d+)/episodes/$', 'json_show_episodes'),
    (r'^json/episode/(?P<episode_id>\d+)/videofiles/$', 'json_episode_videofiles'),
)
