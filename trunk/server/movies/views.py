# Create your views here.
from django.shortcuts import render_to_response
from movies.models import Movie, Genre, Cast, Studio, Country, Person
import datetime

def movies_list(request):
    movies = Movie.objects.all()
    return render_to_response('movies_list.html', {'movies' : movies, })

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    cast = Cast.objects.filter(movie__id=movie_id)
    return render_to_response('movie_detail.html', {'movie' : movie, 'cast' : cast })

def genre_detail(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    movies = genre.movie_set.all()
    return render_to_response('genre_detail.html', {'genre' : genre, 'movies' : movies })

def person_detail(request, person_id):
    person = Person.objects.get(pk=person_id)
    cast = Cast.objects.filter(person__id=person_id)
    return render_to_response('person_detail.html', {'person' : person, 'cast' : cast })

def studio_detail(request, studio_id):
    studio = Studio.objects.get(pk=studio_id)
    movies = studio.movie_set.all()
    return render_to_response('studio_detail.html', {'studio' : studio, 'movies' : movies })

def country_detail(request, country_id):
    country = Country.objects.get(pk=country_id)
    movies = country.movie_set.all()
    return render_to_response('country_detail.html', {'country' : country, 'movies' : movies })
