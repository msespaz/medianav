# Create your views here.
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
import movies.models 
import tv.models


def popcornhour_home(request):
    users = User.objects.all()
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
    videofile = videodirectory.movievideofile_set.all()[0]

    return render_to_response('pch_all.html', locals(), context_instance=RequestContext(request))

def popcornhour_detail(request, movie_id):
    pch_base = settings.MEDIANAV_PCH_MOVIE

    movie = movies.models.Movie.objects.get(pk=movie_id)
    directors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='director').order_by('bill_order')
    actors = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='actor').order_by('bill_order')
    writers = movies.models.Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='writer').order_by('bill_order')
    videodirectory = movie.videodirectory_set.all()[0]
    videofile = videodirectory.movievideofile_set.all()[0]
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

def popcornhour_shows_list(request, username, page_number, selected_id):
    if username == 'all':
        shows = tv.models.Show.objects.all()
    else:
        user = User.objects.get(username=username)
        fav_shows = user.show_set.all()
        unseen_list = []
        for show in fav_shows:
            number_unseen = show.episode_set.filter(tvvideofile__isnull=False).exclude(seen_by=user).count()
            if number_unseen > 0:
                unseen_list.append(show.id)
        shows = tv.models.Show.objects.filter(id__in=unseen_list)

    prefix = 'tv/' + username + '/shows'
    return popcornhour_list(request, username, page_number, selected_id, shows, prefix)

def popcornhour_show_episodes(request, username, show_id, page_number, selected_id):
    
    pch_base = settings.MEDIANAV_PCH_TV

    show = tv.models.Show.objects.get(pk=show_id)
    if username == 'all':
        info = show.name + ' - All episodes'
        episodes = tv.models.Episode.objects.filter(show__id=show_id, tvvideofile__isnull=False).order_by('first_aired')
    else:
        info = show.name + ' - Episodes unwatched by ' + username
        user = User.objects.get(username=username)
        episodes = tv.models.Episode.objects.filter(show__id=show_id, tvvideofile__isnull=False).exclude(seen_by=user).order_by('first_aired')

    if episodes.count() == 0:
#        return redirect('popcornhour_shows_list', username=username, page_number=1, selected_id=0)
        return redirect('/medianav/pch/tv/'+username+'/shows/1/0')

    entries_per_page = 10
    start_entry = entries_per_page * (int(page_number)-1)
    end_entry = start_entry + entries_per_page
    entries_list = episodes[start_entry:end_entry]
    total_entries = episodes.count()

    total_pages = total_entries / entries_per_page
    if total_entries % entries_per_page != 0:
        total_pages = total_pages + 1
    prev_page = int(page_number) - 1
    next_page = int(page_number) + 1
    if prev_page < 1:
        prev_page = 1
        is_first_page = 1
    if next_page > total_pages:
        next_page = total_pages
        is_last_page = 1

    if int(selected_id) == 0:
        selected = entries_list[0]
    else:
        selected = tv.models.Episode.objects.get(pk=selected_id)

    focus = selected.pk
#    videodirectory = selected.tvvideodirectory_set.all()[0]
    videofile = selected.tvvideofile_set.all()[0]

    prefix = 'tv/' + username + '/show/' + show_id + '/episodes'

    return render_to_response('pch_tvepisodes.html', locals(), context_instance=RequestContext(request))

 
def popcornhour_list(request, username, page_number, selected_id, selection, prefix):

    pch_base = settings.MEDIANAV_PCH_TV

    # Collect the list of movies that is available on the current page_number
    entries_per_page = 10
    start_entry = entries_per_page * (int(page_number)-1)
    end_entry = start_entry + entries_per_page
    entries_list = selection[start_entry:end_entry]
    total_entries = selection.count()

    # Generate previous and next page_number, verify they're within range
    # is_first_page and is_last_page are used in the template to determine
    # whether or not the Up and Down links should be shown.
    total_pages = total_entries / entries_per_page
    if total_entries % entries_per_page != 0:
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
    if int(selected_id) == 0:
        selected = entries_list[0] 
    else:
        selected = tv.models.Show.objects.get(pk=selected_id)
    
    focus = selected.pk    
#    videodirectory = selected.videodirectory_set.all()[0]
#    videofile = videodirectory.videofile_set.all()[0]

    return render_to_response('pch_tv.html', locals(), context_instance=RequestContext(request))

def popcornhour_generate_playlist(request, type, username, id):
    if type == 'tv':
        selected = tv.models.Episode.objects.get(pk=id)
        entries = []
        entries.append(settings.MEDIANAV_PCH_TV + '/' + str(selected.tvvideofile_set.all()[0]))
        entries.append( 'http://' + str(Site.objects.get_current()) + '/medianav/tv/json/'+username+'/episode/'+id+'/watched')

    return render_to_response('playlist.jsp', locals(), context_instance=RequestContext(request))

