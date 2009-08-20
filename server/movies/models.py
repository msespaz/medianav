from django.db import models

# Create your models here.

class MovieStatus(models.Model):
    """ Things like Owned, Wish List """
    name = models.CharField(max_length=16, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=16, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)

class Person(models.Model):
    name = models.CharField(max_length=256, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)

class Cast(models.Model):
    person = models.ForeignKey(Person, related_name='cast_person')
    movie = models.ForeignKey('Movie', related_name='cast_movie')
    character = models.CharField(max_length=256, blank=True)
    job = models.CharField(max_length=64, blank=True)

class Studio(models.Model):
    name = models.CharField(max_length=256, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)

class Country(models.Model):
    name = models.CharField(max_length=256, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)

class Movie(models.Model):
    name = models.CharField(max_length=256)
    status = models.ForeignKey(MovieStatus, blank=True, null=True)
    watched = models.BooleanField()
    overview = models.CharField(max_length=4096, blank=True)
    release = models.DateField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    runtime = models.IntegerField(blank=True, null=True)
    trailer_url = models.URLField(verify_exists=False, blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    imdb_id = models.CharField(max_length=16, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)
    moviedb_rating = models.FloatField(blank=True, null=True)
    moviedb_url = models.URLField(verify_exists=False, blank=True)
    moviedb_poster_url = models.URLField(verify_exists=False, blank=True)
    moviedb_backdrop_url = models.URLField(verify_exists=False, blank=True)
    moviedb_last_updated = models.DateField(blank=True, null=True)
    cast = models.ManyToManyField(Person, through='Cast')
    studios = models.ManyToManyField(Studio)
    countries = models.ManyToManyField(Country)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class VideoFormat(models.Model):
    name = models.CharField(max_length=32)

class VideoDirectory(models.Model):
    """ Assumes one movie per directory """
    name = models.CharField(max_length=1024, blank=True)
    format = models.ForeignKey(VideoFormat, blank=True, null=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)

class VideoFile(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)
    format = models.ForeignKey(VideoFormat, blank=True, null=True)
    directory = models.ForeignKey(VideoDirectory, blank=True, null=True)

