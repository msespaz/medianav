# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import movies.models 
import tv.models


def popcornhour_home(request):
    return render_to_response('pch_home.html', locals(), context_instance=RequestContext(request))

def popcornhour_all(request, page_number, movie_id):
    
    movies_selection = movies.models.Movie.objects.all()
    prefix = 'all'
    return popcornhour_list_movies(request, page_number, movie_id, movies_selection, prefix)

def popcornhour_genre(request, page_number, movie_id, genre_id):
    genre = movies.models.Genre.objects.get(pk=genre_id)
    movies_selection = genre.movie_set.all()
    prefix = 'genre/' + genre_id
    return popcornhour_list_movies(request, page_number, movie_id, movies_selection, prefix)

def popcornhour_list_movies(request, page_number, movie_id, movies_selection, prefix):

    pch_base = settings.MEDIANAV_PCH_MOVIE

    # Collect the list of movies that is available on the current page_number
    movies_per_page = 10
    start_movie = movies_per_page * (int(page_number)-1)
    end_movie = start_movie + movies_per_page
    movies_list = movies_selection[start_movie:end_movie]
    total_movies = movies_selection.count()

    # Generate previous and next page_number, verify they're within range
    # is_first_page and is_last_page are used in the template to determine
    # whether or not the Up and Down links should be shown.
    total_pages = total_movies / movies_per_page
    if total_movies % movies_per_page != 0:
        total_pages = total_pages + 1
    prev_page = int(page_number) - 1
    next_page = int(page_number) + 1
    if prev_page < 1:
        prev_page = 1
	is_first_page = 1
    if next_page > total_pages:
        next_page = total_pages
        is_last_page = 1

    # Set the focus to the top of the list if movie_id = 0 (the default when entering the browser)
	# or set the focus to the select movie_id
    if int(movie_id) == 0:
        selected = movies_list[0] 
    else:
        selected = movies.models.Movie.objects.get(pk=movie_id)
    
    focus = selected.pk    
    videodirectory = selected.videodirectory_set.all()[0]
    videofile = videodirectory.videofile_set.all()[0]

    return render_to_response('pch_all.html', locals(), context_instance=RequestContext(request))

def popcornhour_detail(request, movie_id):
    pch_base = settings.MEDIANAV_PCH_MOVIE

    movie = movies.models.Movie.objects.get(pk=movie_id)
    directors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='director').order_by('bill_order')
    actors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='actor').order_by('bill_order')
    writers = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='writer').order_by('bill_order')
    videodirectory = movie.videodirectory_set.all()[0]
    videofile = videodirectory.videofile_set.all()[0]
    return render_to_response('pch_detail.html', locals(), context_instance=RequestContext(request))

def popcornhour_genre_list(request, page_number, genre_id):
    genres_per_page = 10
    start_genre = genres_per_page * (int(page_number)-1)
    end_genre = start_genre + genres_per_page
    genres_list = movies.models.Genre.objects.all().order_by('name')[start_genre:end_genre]
    total_genres = movies.models.Genre.objects.all().count()

    total_pages = total_genres / genres_per_page
    if total_genres % genres_per_page != 0:
        total_pages = total_pages + 1
    prev_page = int(page_number) - 1
    next_page = int(page_number) + 1
    if prev_page < 1:
        prev_page = 1
        is_first_page = 1
    if next_page > total_pages:
        next_page = total_pages
        is_last_page = 1

    if int(genre_id) == 0:
        selected = genres_list[0]
    else:
        selected = movies.models.Genre.objects.get(pk=genre_id)

    focus = selected.pk

    filter_desc = 'Genre'

    return render_to_response('pch_filter.html', locals(), context_instance=RequestContext(request))

