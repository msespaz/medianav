from django.db import models


from django.db.models.fields import IntegerField
from django.conf import settings

import re

# Custom big integer field
class BigIntegerField(IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"
                        
    def db_type(self):
        return 'NUMBER(19)' if settings.DATABASE_ENGINE == 'oracle' else 'bigint'

# Create your models here.

class MovieStatus(models.Model):
    """ Things like Owned, Wish List """
    name = models.CharField(max_length=16, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=16, blank=True)

    def short_name(self):
        """ Returns a short name for the genre """
        return self.name[:3]
    
    def __unicode__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=32, blank=True)
    
    def __unicode__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=256, blank=True)
    imdb_id = models.CharField(max_length=32, blank=True)
    
    def imdb_link(self):
        """ Returns a URL to the imdb page """
        return 'http://www.imdb.com/name/nm%s/' % self.imdb_id
    
    def __unicode__(self):
        return self.name

class Cast(models.Model):
    person = models.ForeignKey(Person, related_name='cast_person')
    movie = models.ForeignKey('Movie', related_name='cast_movie')
    role = models.CharField(max_length=1024, blank=True)
    job = models.CharField(max_length=64, blank=True)
    bill_order = models.IntegerField(blank=True, null=True) # Order as it appears in imdb
    
    def __unicode__(self):
        return "%s - %s - %s" % (self.person.name, self.movie.title, self.job)

class Company(models.Model):
    name = models.CharField(max_length=256, blank=True)
    imdb_id = models.CharField(max_length=32, blank=True)
    
    def imdb_link(self):
        """ Returns a URL to the imdb page """
        return 'http://www.imdb.com/company/co%s/' % self.imdb_id
    
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=256, blank=True)
    
    def __unicode__(self):
        return self.name

class Movie(models.Model):
    # This model is based on the imdb model from imdbpy
    title = models.CharField(max_length=256)
    imdb_id = models.CharField(max_length=16, blank=True)
    imdb_last_updated = models.DateTimeField(blank=True, null=True)
    imdb_long_title = models.CharField(max_length=256, blank=True)
    canon_title = models.CharField(max_length=256, blank=True)
    imdb_canon_long_title = models.CharField(max_length=256, blank=True)
    year = models.IntegerField(blank=True, null=True)
    imdb_kind = models.CharField(max_length=16, blank=True) # One of movie, tv series, tv mini series, video game, video movie, tv movie, episode
    imdb_index = models.CharField(max_length=16, blank=True) # roman number for movies with the same title/year
   
    cast = models.ManyToManyField(Person, through='Cast') # The cast contains directors, writers and actors
    imdb_cover_url = models.URLField(verify_exists=False, blank=True)
    plot = models.CharField(max_length=4096, blank=True)
    plot_outline = models.CharField(max_length=4096, blank=True)
    imdb_rating = models.FloatField(blank=True, null=True)
    imdb_votes = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    countries = models.ManyToManyField(Country)
    genres = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    certificates = models.ManyToManyField(Certificate)
    mpaa = models.CharField(max_length=255, blank=True)
    production_companies = models.ManyToManyField(Company)

    status = models.ForeignKey(MovieStatus, blank=True, null=True)
    watched = models.DateTimeField(blank=True, null=True)

    #overview = models.CharField(max_length=4096, blank=True)
    #release = models.DateField(blank=True, null=True)
    trailer_url = models.URLField(verify_exists=False, blank=True)
    #homepage = models.URLField(verify_exists=False, blank=True)
    moviedb_id = models.IntegerField(blank=True, null=True)
    moviedb_rating = models.FloatField(blank=True, null=True)
    moviedb_url = models.URLField(verify_exists=False, blank=True)
    moviedb_poster_url = models.URLField(verify_exists=False, blank=True)
    moviedb_backdrop_url = models.URLField(verify_exists=False, blank=True)
    moviedb_last_updated = models.DateField(blank=True, null=True)

    def imdb_link(self):
        """ Returns a URL to the imdb page """
        return 'http://www.imdb.com/title/tt%s/' % self.imdb_id

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.year)


class VideoFormat(models.Model):
    name = models.CharField(max_length=32)

class VideoDirectory(models.Model):
    """ Assumes one movie per directory """
    name = models.CharField(max_length=1024, blank=True)
    format = models.ForeignKey(VideoFormat, blank=True, null=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)

    def get_size(self):
        total_size = 0
        for videofile in self.videofile_set.all():
            total_size += videofile.file_size
        return total_size

    def main_video(self):
        return self.videofile_set.all().order_by('-file_size')[0]

    def format_name(self):
        """ Generate a name for this directory """
        return "%s (%s%s) %s" % (
                re.sub(r'[^\w \(\)\-]', '', self.movie.title),
                self.movie.year,
                self.movie.imdb_index,
                self.main_video().format_name()
                )
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return '%s' % (self.name)

class VideoFile(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    movie = models.ForeignKey(Movie, blank=True, null=True)
    directory = models.ForeignKey(VideoDirectory, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    file_size = BigIntegerField(blank=True, null=True)
    # Media Info fields
    audio_bitrate = BigIntegerField(blank=True, null=True)
    audio_channels = models.IntegerField(blank=True, null=True)
    audio_codec = models.CharField(max_length=32, blank=True)
    audio_codec_id = models.CharField(max_length=32, blank=True)
    audio_format = models.CharField(max_length=32, blank=True)
    audio_language = models.CharField(max_length=32, blank=True)
    audio_resolution = models.IntegerField(blank=True, null=True)
    audio_samplerate = models.IntegerField(blank=True, null=True)
    general_bitrate = BigIntegerField(blank=True, null=True)
    general_codec = models.CharField(max_length=32, blank=True)
    general_duration = models.IntegerField(blank=True, null=True)
    general_format = models.CharField(max_length=32, blank=True)
    general_size = BigIntegerField(blank=True, null=True)
    video_bitrate = BigIntegerField(blank=True, null=True)
    video_codec = models.CharField(max_length=32, blank=True)
    video_codec_id = models.CharField(max_length=32, blank=True)
    video_displayaspect = models.FloatField(blank=True, null=True)
    video_pixelaspect = models.FloatField(blank=True, null=True)
    video_format = models.CharField(max_length=32, blank=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_scantype = models.CharField(max_length=32, blank=True)

    def audio_name(self):
        """ Returns a name for the audio """
        if self.audio_codec in ('AC3', 'DTS'):
            return self.audio_codec
        if self.audio_format in ('AAC', 'WMA3'):
            return self.audio_format
        if self.audio_codec == 'MPA1L3':
            return 'MP3'
        if self.audio_codec == 'MPA1L2':
            return 'MP2'
        if self.audio_format == 'MPEG Audio':
            return 'MPA'
        if self.audio_codec:
            return self.audio_codec.split('/')[0]
        return '-'

    def video_name(self):
        """ Returns a name for the video """
        if self.video_codec in ('XVID', 'DX50', 'DIV3', 'DIVX', 'div3'):
            return 'DIVX'
        if self.video_codec == 'MPEG-2V':
            return 'MPG2'
        if self.video_codec == 'MPEG-1V':
            return 'MPG1'
        if self.video_format == 'AVC':
            return 'AVC'
        if self.video_format == 'VC-1':
            return 'VC1'
        if self.video_codec == 'MP42':
            return 'MP4'
        if self.video_codec:
            return self.video_codec.split('/')[0]
        return '-'

    def video_def(self):
        """ Returns a name for the definition of the video 
            Not all videos conform to the standards, so some assumptions
            are made and ranges are used
        """

        if self.video_width >= 1440:
            return "HD1080"
        if self.video_width >= 960:
            return "HD720"
        if self.video_width >= 720:
            # this is a DVD
            if self.video_height == 480:
                return 'DVDNTSC'
            if self.video_height == 576:
                return 'DVDPAL'
            else:
                return 'DVD'
        if self.video_width >= 700:
            return "SD7"
        if self.video_width >= 600:
            return "SD6"
        if self.video_width >= 500:
            return "SD5"
        if self.video_width >= 400:
            return "SD4"
        if self.video_width >= 300:
            return "SD3"
        if self.video_width >= 200:
            return "SD2"
        if self.video_width >= 100:
            return "SD1"
        return "-"

    def audio_chan_name(self):
        """ Returns a name for the number of channels """
        if self.audio_channels >= 4:
            return "SUR"
        if self.audio_channels == 2:
            return "STEREO"
        if self.audio_channels == 1:
            return "MONO"
        return '-'

    def extension_name(self):
        """ Returns the name of the file extension """
        return self.name.split('.')[-1].upper()

    def format_name(self):
        return '%s %s %s %s %s' % (
                self.video_def(),
                self.audio_chan_name(),
                self.extension_name(),
                self.video_name(),
                self.audio_name()
                )

    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return '%s' % (self.name)

