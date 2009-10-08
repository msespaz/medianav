# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from tv.models import Show, Episode, VideoFile
from django.core import serializers
from django.contrib.auth.models import User
import datetime


def shows_list(request):
    return handle_shows_list(request, False)

def favourite_list(request):
    return handle_shows_list(request, True)

def handle_shows_list(request, fav_only=False):
    if request.method == 'POST':
        favs = []
        for fav in request.POST.getlist('fav'):
            favs.append(Show.objects.get(pk=fav))
        request.user.show_set = favs
    if fav_only:
        shows = Show.objects.filter(fav_of=request.user)
    else:
        shows = Show.objects.all()
    for show in shows:
        if request.user in show.fav_of.all():
            show.is_fav = True
        else:
            show.is_fav = False
    return render_to_response('shows_list.html', locals(), context_instance=RequestContext(request))

def show_detail(request, show_id):
    # Get show detail and list of episodes
    show = Show.objects.get(pk=show_id)
    episodes = show.episode_set.all()

    # If this is a post, update the list of seen episodes 
    if request.method == 'POST':
        for episode in episodes:
            request.user.episode_set.remove(episode)
        for s in request.POST.getlist('seen'):
            request.user.episode_set.add(Episode.objects.get(pk=s))

    # Add watched flag to episode
    for episode in episodes:
        if request.user in episode.seen_by.all():
            episode.seen = True
        else:
            episode.seen = False

    return render_to_response('show_detail.html', locals(), context_instance=RequestContext(request))

def episode_detail(request, episode_id):
    episode = Episode.objects.get(pk=episode_id)
    return render_to_response('episode_detail.html', locals(), context_instance=RequestContext(request))

def missing_episodes(request):
    # A list of episodes for which there are no files
    # Only pulls up a list for the last year and excludes specials
    episodes = Episode.objects.filter(season_number__gt=0, first_aired__gt=datetime.date.today()-datetime.timedelta(weeks=52), videofile__isnull=True).order_by('first_aired')
    return render_to_response('missing_episodes.html', locals(), context_instance=RequestContext(request))

def json_show_episodes(request, show_id, username='all'):
    """ Returns a json result with a list of episodes for a particular show """
    if username == 'all':
        episodes = Episode.objects.filter(show__id=show_id, videofile__isnull=False).order_by('first_aired')
    else:
        user = User.objects.get(username=username)
        episodes = Episode.objects.filter(show__id=show_id, videofile__isnull=False).exclude(seen_by=user).order_by('first_aired')
    return HttpResponse(serializers.serialize('json', episodes, fields=('tvdb_image','overview', 'episode_number', 'season_number', 'first_aired', 'name')), content_type='application/json')

def json_episode_watched(request, username, episode_id):
    user = User.objects.get(username=username)
    episode = Episode.objects.get(pk=episode_id)
    user.episode_set.add(episode)
    return HttpResponse(serializers.serialize('json', [episode]), content_type='application/json')

def json_shows_list(request, username='all'):
    """ Returns a list of shows in json """
    if username == 'all':
        shows = Show.objects.all()
    else:
        user = User.objects.get(username=username)
        fav_shows = user.show_set.all()
        unseen_list = []
        for show in fav_shows:
            number_unseen = show.episode_set.filter(videofile__isnull=False).exclude(seen_by=user).count()
            if number_unseen > 0:
                unseen_list.append(show.id)
        shows = Show.objects.filter(id__in=unseen_list)

    return HttpResponse(serializers.serialize('json', shows, fields=('name', 'tvdb_showid')), content_type='application/json')

def json_episode_videofiles(request, episode_id):
    """ Returns a json result with a list of episodes for a particular show """
    videofiles = VideoFile.objects.filter(episodes__id=episode_id)
    return HttpResponse(serializers.serialize('json', videofiles, fields=('name')), content_type='application/json')
