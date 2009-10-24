from django.conf.urls.defaults import *

urlpatterns = patterns('pch.views',
    (r'^$', 'popcornhour_home'),
    (r'^all/(?P<page_number>\d+)/(?P<movie_id>\d+)/$', 'popcornhour_all'),
    (r'^detail/(?P<movie_id>\d+)/$', 'popcornhour_detail'),
    (r'^genre/(?P<genre_id>\d+)/(?P<page_number>\d+)/(?P<movie_id>\d+)/$', 'popcornhour_genre'),
    (r'^genre_list/(?P<page_number>\d+)/(?P<genre_id>\d+)/$', 'popcornhour_genre_list'),

    (r'^tv/(?P<username>\w+)/shows/(?P<page_number>\d+)/(?P<selected_id>\d+)/$', 'popcornhour_shows_list'),
    (r'^tv/(?P<username>\w+)/show/(?P<show_id>\d+)/episodes/(?P<page_number>\d+)/(?P<selected_id>\d+)/$', 'popcornhour_show_episodes'),
    (r'^(?P<type>\w+)/(?P<username>\w+)/(?P<id>\d+)/playlist.jsp$', 'popcornhour_generate_playlist'),

#        (r'^json/(?P<username>\w+)/show/(?P<show_id>\d+)/episodes/$', 'json_show_episodes'),

#    (r'^json/(?P<username>\w+)/episode/(?P<episode_id>\d+)/watched/$', 'json_episode_watched'),
#    http://192.168.2.100:8000/medianav/pch/tv/all/shows/1/0
#    http://192.168.2.100:8000/medianav/pch/tv/andre/shows/1/0


)
