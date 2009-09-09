from django.conf.urls.defaults import *

urlpatterns = patterns('movies.views',
    (r'^$', 'movies_list'),
    (r'^movie/(?P<movie_id>\d+)/$', 'movie_detail'),
    (r'^genre/(?P<genre_id>\d+)/$', 'genre_detail'),
    (r'^person/(?P<person_id>\d+)/$', 'person_detail'),
    (r'^company/(?P<company_id>\d+)/$', 'company_detail'),
    (r'^country/(?P<country_id>\d+)/$', 'country_detail'),

    (r'^json/movie/(?P<movie_id>\d+)/$', 'json_movie_detail'),
    (r'^json/movies/$', 'json_movies_list'),
    (r'^json/genres/$', 'json_genre_list'),
    (r'^json/movie/(?P<movie_id>\d+)/directories/$', 'json_movie_directories'),
    (r'^json/directory/(?P<directory_id>\d+)/videofiles/$', 'json_directory_videofiles'),
)
