from django.db import models
import mnav.fields
import os
import stat
import datetime
from mnav.mediainfo import parse_info

class BaseVideoFile(models.Model):
    """ A videofile model that can be used in other apps """
    name = models.CharField(max_length=1024, blank=True)
    ctime = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    file_size = mnav.fields.BigIntegerField(blank=True, null=True)
    # Media Info fields
    audio_bitrate = mnav.fields.BigIntegerField(blank=True, null=True)
    audio_channels = models.IntegerField(blank=True, null=True)
    audio_codec = models.CharField(max_length=32, blank=True)
    audio_codec_id = models.CharField(max_length=32, blank=True)
    audio_format = models.CharField(max_length=32, blank=True)
    audio_language = models.CharField(max_length=32, blank=True)
    audio_resolution = models.IntegerField(blank=True, null=True)
    audio_samplerate = models.IntegerField(blank=True, null=True)
    general_bitrate = mnav.fields.BigIntegerField(blank=True, null=True)
    general_codec = models.CharField(max_length=32, blank=True)
    general_duration = models.IntegerField(blank=True, null=True)
    general_format = models.CharField(max_length=32, blank=True)
    general_size = mnav.fields.BigIntegerField(blank=True, null=True)
    video_bitrate = mnav.fields.BigIntegerField(blank=True, null=True)
    video_codec = models.CharField(max_length=32, blank=True)
    video_codec_id = models.CharField(max_length=32, blank=True)
    video_displayaspect = models.FloatField(blank=True, null=True)
    video_pixelaspect = models.FloatField(blank=True, null=True)
    video_format = models.CharField(max_length=32, blank=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_scantype = models.CharField(max_length=32, blank=True)

    @property
    def absolute_path(self):
        """ Returns the absolute path of the file 
            Override this function when you use BaseVideoFile in another class
        """
        return self.name

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

    def update_mediainfo(self, force=False):
        """ Update the mediainfo for the videofile 
            Note, this does not save the instance, you still have to call save() for that
        """
        fullpath = self.absolute_path
        s=os.stat(fullpath)
        if self.last_updated and (not force) and datetime.datetime.fromtimestamp(s[stat.ST_MTIME]) <= self.last_updated:
            return False
        self.ctime=datetime.datetime.fromtimestamp(s[stat.ST_CTIME])
        self.file_size=s[stat.ST_SIZE]
        self.last_updated = datetime.datetime.now()

        mi = parse_info(fullpath)
        if mi['audio_bitrate']: self.audio_bitrate = int(mi['audio_bitrate'])
        if mi['audio_channels']: self.audio_channels = int(mi['audio_channels'])
        self.audio_codec = mi['audio_codec']
        self.audio_codec_id = mi['audio_codec_id']
        self.audio_format = mi['audio_format']
        self.audio_language = mi['audio_language']
        if mi['audio_resolution']: self.audio_resolution = int(mi['audio_resolution']) 
        if mi['audio_samplerate']: self.audio_samplerate = int(mi['audio_samplerate'])
        if mi['general_bitrate']: self.general_bitrate = int(mi['general_bitrate'])
        self.general_codec = mi['general_codec']
        if mi['general_duration']: self.general_duration = int(mi['general_duration'])
        self.general_format = mi['general_format']
        if mi['general_size']: self.general_size = int(mi['general_size'])
        if mi['video_bitrate']: self.video_bitrate = int(mi['video_bitrate'])
        self.video_codec = mi['video_codec']
        self.video_codec_id = mi['video_codec_id']
        if mi['video_displayaspect']: self.video_displayaspect = float(mi['video_displayaspect'])
        if mi['video_pixelaspect']: self.video_pixelaspect = float(mi['video_pixelaspect'])
        self.video_format = mi['video_format']
        if mi['video_width']: self.video_width = int(mi['video_width'])
        if mi['video_height']: self.video_height = int(mi['video_height'])
        self.video_scantype = mi['video_scantype']
        return True

