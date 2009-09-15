from django.conf.urls.defaults import *

urlpatterns = patterns('tv.views',
    (r'^$', 'shows_list'),
    (r'^favourite/$', 'favourite_list'),
    (r'^show/(?P<show_id>\d+)/$', 'show_detail'),
    (r'^episode/(?P<episode_id>\d+)/$', 'episode_detail'),
    (r'^missing/$', 'missing_episodes'),
    (r'^json/(?P<username>\w+)/shows/$', 'json_shows_list'),
    (r'^json/(?P<username>\w+)/show/(?P<show_id>\d+)/episodes/$', 'json_show_episodes'),
    (r'^json/episode/(?P<episode_id>\d+)/videofiles/$', 'json_episode_videofiles'),
)
