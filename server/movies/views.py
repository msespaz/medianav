# Create your views here.
from django.shortcuts import render_to_response
from movies.models import *
import datetime

def movies_list(request):
    movies = Movie.objects.all()
    return render_to_response('movies_list.html', {'movies' : movies, })

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    directors = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='director').order_by('bill_order')
    actors = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='actor').order_by('bill_order')
    writers = Cast.objects.filter(movie__id=movie_id, bill_order__lt=15, job='writer').order_by('bill_order')
    return render_to_response('movie_detail.html', {'movie' : movie, 'actors' : actors, 'directors' : directors, 'writers' : writers })

def genre_detail(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    movies = genre.movie_set.all()
    return render_to_response('genre_detail.html', {'genre' : genre, 'movies' : movies })
    return None

def person_detail(request, person_id):
    person = Person.objects.get(pk=person_id)
    cast = Cast.objects.filter(person__id=person_id).order_by('movie__year')
    return render_to_response('person_detail.html', {'person' : person, 'cast' : cast })
    return None

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    movies = company.movie_set.all()
    return render_to_response('company_detail.html', {'company' : company, 'movies' : movies })
    return None

def country_detail(request, country_id):
    country = Country.objects.get(pk=country_id)
    movies = country.movie_set.all()
    return render_to_response('country_detail.html', {'country' : country, 'movies' : movies })
    return None
