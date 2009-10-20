from django.conf.urls.defaults import *

urlpatterns = patterns('pch.views',
    (r'^$', 'popcornhour_home'),
    (r'^all/(?P<page_number>\d+)/(?P<movie_id>\d+)/$', 'popcornhour_all'),
    (r'^detail/(?P<movie_id>\d+)/$', 'popcornhour_detail'),
    (r'^genre/(?P<genre_id>\d+)/(?P<page_number>\d+)/(?P<movie_id>\d+)/$', 'popcornhour_genre'),
    (r'^genre_list/(?P<page_number>\d+)/(?P<genre_id>\d+)/$', 'popcornhour_genre_list'),
    
)
