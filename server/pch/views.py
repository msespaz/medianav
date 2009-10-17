# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import movies.models 
import tv.models


def popcornhour_home(request):
    return render_to_response('pch_home.html', locals(), context_instance=RequestContext(request))

def popcornhour_all(request, page_number, movie_id):

    pch_base = settings.MEDIANAV_PCH_MOVIE

    # Collect the list of movies that is available on the current page_number
    movies_per_page = 10
    start_movie = movies_per_page * (int(page_number)-1)
    end_movie = start_movie + movies_per_page
    movies_list = movies.models.Movie.objects.all()[start_movie:end_movie]
    total_movies =  movies.models.Movie.objects.all().count()

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
        focus = movies_list[0].pk
        poster = movies_list[0].moviedb_id
        plot = movies_list[0].plot_outline
        videodirectory = movies_list[0].videodirectory_set.all()[0]
        videofile = videodirectory.videofile_set.all()[0]
    else:
        focus = int(movie_id)
        temp = movies.models.Movie.objects.get(pk=movie_id)
        poster = temp.moviedb_id
        plot = temp.plot_outline
        videodirectory = temp.videodirectory_set.all()[0]
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

