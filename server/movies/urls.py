from django.conf.urls.defaults import *
from django.views import static

urlpatterns = patterns('movies.views',
    (r'^$', 'movies_list'),
    (r'^movie/(?P<movie_id>\d+)/$', 'movie_detail'),
    (r'^genre/(?P<genre_id>\d+)/$', 'genre_detail'),
    (r'^person/(?P<person_id>\d+)/$', 'person_detail'),
    (r'^company/(?P<company_id>\d+)/$', 'company_detail'),
    (r'^country/(?P<country_id>\d+)/$', 'country_detail'),
    (r'^media/(?P<path>.*)$', static.serve, {'document_root': 'movies/media', 'show_indexes': True}),
)
