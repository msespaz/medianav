# Create your views here.
from django.shortcuts import render_to_response
from tv.models import Show, Episode
import datetime

def shows_list(request):
    shows = Show.objects.all()
    return render_to_response('shows_list.html', {'shows' : shows, })

def show_detail(request, show_id):
    show = Show.objects.get(pk=show_id)
    return render_to_response('show_detail.html', {'show' : show, })

def episode_detail(request, episode_id):
    episode = Episode.objects.get(pk=episode_id)
    return render_to_response('episode_detail.html', {'episode' : episode, })

def missing_episodes(request):
    # A list of episodes for which there are no files
    # Only pulls up a list for the last year and excludes specials
    episodes = Episode.objects.filter(season_number__gt=0, first_aired__gt=datetime.date.today()-datetime.timedelta(weeks=52), videofile__isnull=True).order_by('first_aired')
    return render_to_response('missing_episodes.html', {'episodes' : episodes, })
