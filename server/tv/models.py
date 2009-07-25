from django.db import models
import datetime

# Create your models here.

class Show(models.Model):
    # Common fields. We are really getting this information
    # from thetvdb.com, but in theory you could get them elsewhere
    name = models.CharField(max_length=256)
    overview = models.CharField(max_length=4024, blank=True)
    genre = models.CharField(max_length=32, blank=True)
    network = models.CharField(max_length=32, blank=True)
    content_rating = models.CharField(max_length=16, blank=True)
    runtime = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True)
    first_aired = models.DateField(blank=True, null=True)
    airs_day = models.CharField(max_length=16, blank=True)
    airs_time = models.TimeField(blank=True, null=True)
    # TVDB Specific fields
    tvdb_language = models.CharField(max_length=16, blank=True)
    tvdb_showid = models.IntegerField(blank=True, null=True)
    tvdb_rating = models.FloatField(blank=True, null=True)
    tvdb_banner_url = models.URLField(verify_exists=False, blank=True)
    tvdb_poster_url = models.URLField(verify_exists=False, blank=True)
    tvdb_fanart_url = models.URLField(verify_exists=False, blank=True)
    tvdb_last_updated = models.DateTimeField(blank=True, null=True) 

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class AlternateShowName(models.Model):
    # Alternate names for TV shows, used in identifying them during a scan
    name = models.CharField(max_length=256)
    show = models.ForeignKey(Show, blank=True)
    priority = models.IntegerField(default=100)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s=%s" % (self.name, self.show.name)

class VideoFilePattern(models.Model):
    # Regular expression patterns, used by the scanner to find information
    # such as show name, season and episode number from the filename
    re = models.CharField(max_length=1024)
    priority = models.IntegerField(default=100)
    description = models.CharField(max_length=1024)
    
    class Meta:
        ordering = ['priority']
    
    def __unicode__(self):
        return "%s - %s" % (self.description[:16], self.re[:16])


class Episode(models.Model):
    # Common fields. We are really getting this information
    # from thetvdb.com, but in theory you could get them elsewhere
    name = models.CharField(max_length=256, blank=True)
    overview = models.CharField(max_length=4024, blank=True)
    season_number = models.IntegerField(blank=True, null=True)
    episode_number = models.IntegerField(blank=True, null=True)
    director = models.CharField(max_length=256, blank=True)
    guest_stars = models.CharField(max_length=1024, blank=True)
    production_code = models.CharField(max_length=64, blank=True)
    writer = models.CharField(max_length=256, blank=True)
    show = models.ForeignKey(Show, blank=True)
    first_aired = models.DateField(blank=True, null=True)
    # TVDB Specific fields
    tvdb_episodeid = models.IntegerField(blank=True, null=True)
    tvdb_language = models.CharField(max_length=16, blank=True)
    tvdb_rating = models.FloatField(blank=True, null=True)
    tvdb_image = models.URLField(verify_exists=False, blank=True)
    tvdb_last_updated = models.DateTimeField(blank=True, null=True) 

    def newzbin_url(self):
        # Returns a url to search for the episode on newzbin
        return "http://v3.newzbin.com/search/query/?q=%s+%dx%02d&area=-1&fpn=p&searchaction=Go&areadone=-1" % (self.show.name.lower().replace(' ','+').replace('&',''), self.season_number, self.episode_number)

    def air_status(self):
        # Returns if this episode has aired already
        if self.first_aired < datetime.date.today():
            return "aired"
        elif self.first_aired > datetime.date.today():
            return "notaired"
        else:
            return "today"

    class Meta:
        ordering = ['show__name', 'season_number', 'episode_number', 'name']

    def __unicode__(self):
        return "s%02de%02d %s" % (self.season_number, self.episode_number, self.name)

class VideoFile(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    show = models.ForeignKey(Show, blank=True, null=True)
    episodes = models.ManyToManyField(Episode)
    
    class Meta:
        ordering = ['show__name', 'name']

    def __unicode__(self):
        return self.name
