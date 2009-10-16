# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import movies.models 
import tv.models


def popcornhour_home(request):
    return render_to_response('pch_home.html', locals(), context_instance=RequestContext(request))

def popcornhour_all(request, page_number):
    movies_per_page = 10
    start_movie = movies_per_page * (int(page_number)-1)
    end_movie = start_movie + movies_per_page
    movies_list = movies.models.Movie.objects.all()[start_movie:end_movie]
    total_movies =  movies.models.Movie.objects.all().count()
    focus = movies_list[0].pk
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
    return render_to_response('pch_all.html', locals(), context_instance=RequestContext(request))

def popcornhour_detail(request, movie_id):
    movie = movies.models.Movie.objects.get(pk=movie_id)
    directors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='director').order_by('bill_order')
    actors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='actor').order_by('bill_order')
    writers = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='writer').order_by('bill_order')
    videodirectory = movie.videodirectory_set.all()[0]
    videofile = videodirectory.videofile_set.all()[0]
    return render_to_response('pch_detail.html', locals(), context_instance=RequestContext(request))

