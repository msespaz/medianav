
from south.db import db
from django.db import models
from movies.models import *

class Migration:
    # During a dry the ORM cannot be accessed
    # since this whole migration is a data migration
    # disable dry runs
    no_dry_run = True

    def forwards(self, orm):
        # copy videofiles from old model to the new
        for o in orm['movies.VideoFile'].objects.all():
            new = orm.MovieVideoFile(movie=o.movie, directory=o.directory)
            new.basevideofile_ptr = orm['mnav.BaseVideoFile'].objects.create()
            new.basevideofile_ptr.name = o.name
            new.basevideofile_ptr.ctime = o.ctime
            new.basevideofile_ptr.last_updated = o.last_updated
            new.basevideofile_ptr.file_size = o.file_size
            new.basevideofile_ptr.audio_bitrate = o.audio_bitrate
            new.basevideofile_ptr.audio_channels = o.audio_channels
            new.basevideofile_ptr.audio_codec = o.audio_codec
            new.basevideofile_ptr.audio_codec_id = o.audio_codec_id
            new.basevideofile_ptr.audio_format = o.audio_format
            new.basevideofile_ptr.audio_language = o.audio_language
            new.basevideofile_ptr.audio_resolution = o.audio_resolution
            new.basevideofile_ptr.audio_samplerate = o.audio_samplerate
            new.basevideofile_ptr.general_bitrate = o.general_bitrate
            new.basevideofile_ptr.general_codec = o.general_codec
            new.basevideofile_ptr.general_duration = o.general_duration
            new.basevideofile_ptr.general_format = o.general_format
            new.basevideofile_ptr.general_size = o.general_size
            new.basevideofile_ptr.video_bitrate = o.video_bitrate
            new.basevideofile_ptr.video_codec = o.video_codec
            new.basevideofile_ptr.video_codec_id = o.video_codec_id
            new.basevideofile_ptr.video_displayaspect = o.video_displayaspect
            new.basevideofile_ptr.video_pixelaspect = o.video_pixelaspect
            new.basevideofile_ptr.video_format = o.video_format
            new.basevideofile_ptr.video_width = o.video_width
            new.basevideofile_ptr.video_height = o.video_height
            new.basevideofile_ptr.video_scantype = o.video_scantype
            new.basevideofile_ptr.save()
            new.save()
    
    def backwards(self, orm):
        # Copy data from new model back to old one
        for o in orm.MovieVideoFile.objects.all():
            new = orm.VideoFile()
            new.directory = o.directory
            new.movie = o.movie
            new.name = o.basevideofile_ptr.name
            new.ctime = o.basevideofile_ptr.ctime
            new.last_updated = o.basevideofile_ptr.last_updated
            new.file_size = o.basevideofile_ptr.file_size
            new.audio_bitrate = o.basevideofile_ptr.audio_bitrate
            new.audio_channels = o.basevideofile_ptr.audio_channels
            new.audio_codec = o.basevideofile_ptr.audio_codec
            new.audio_codec_id = o.basevideofile_ptr.audio_codec_id
            new.audio_format = o.basevideofile_ptr.audio_format
            new.audio_language = o.basevideofile_ptr.audio_language
            new.audio_resolution = o.basevideofile_ptr.audio_resolution
            new.audio_samplerate = o.basevideofile_ptr.audio_samplerate
            new.general_bitrate = o.basevideofile_ptr.general_bitrate
            new.general_codec = o.basevideofile_ptr.general_codec
            new.general_duration = o.basevideofile_ptr.general_duration
            new.general_format = o.basevideofile_ptr.general_format
            new.general_size = o.basevideofile_ptr.general_size
            new.video_bitrate = o.basevideofile_ptr.video_bitrate
            new.video_codec = o.basevideofile_ptr.video_codec
            new.video_codec_id = o.basevideofile_ptr.video_codec_id
            new.video_displayaspect = o.basevideofile_ptr.video_displayaspect
            new.video_pixelaspect = o.basevideofile_ptr.video_pixelaspect
            new.video_format = o.basevideofile_ptr.video_format
            new.video_width = o.basevideofile_ptr.video_width
            new.video_height = o.basevideofile_ptr.video_height
            new.video_scantype = o.basevideofile_ptr.video_scantype
            new.save()

    models = {
        'mnav.basevideofile': {
            'audio_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_channels': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_codec_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_language': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_resolution': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_samplerate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'file_size': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'general_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'general_size': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'video_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_codec_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_displayaspect': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'video_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_pixelaspect': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'video_scantype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'movies.cast': {
            'bill_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cast_movie'", 'to': "orm['movies.Movie']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cast_person'", 'to': "orm['movies.Person']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        'movies.certificate': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'movies.company': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'movies.country': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'movies.genre': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        'movies.language': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'movies.movie': {
            'canon_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Person']"}),
            'certificates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Certificate']"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Country']"}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_canon_long_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'imdb_cover_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'imdb_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'imdb_kind': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'imdb_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'imdb_long_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'imdb_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'imdb_votes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Language']"}),
            'moviedb_backdrop_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'moviedb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'moviedb_last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'moviedb_poster_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'moviedb_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'moviedb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mpaa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'plot': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'plot_outline': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'production_companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['movies.Company']"}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.MovieStatus']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'trailer_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'watched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'movies.moviestatus': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        'movies.movievideofile': {
            'basevideofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mnav.BaseVideoFile']", 'unique': 'True', 'primary_key': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.VideoDirectory']", 'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.Movie']", 'null': 'True', 'blank': 'True'})
        },
        'movies.person': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'movies.videodirectory': {
            'ctime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.VideoFormat']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.Movie']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        'movies.videofile': {
            'audio_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_channels': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_codec_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_language': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'audio_resolution': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audio_samplerate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.VideoDirectory']", 'null': 'True', 'blank': 'True'}),
            'file_size': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'general_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'general_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'general_size': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['movies.Movie']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'video_bitrate': ('mnav.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_codec': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_codec_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_displayaspect': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'video_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_pixelaspect': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'video_scantype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'video_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'movies.videoformat': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }
    
    complete_apps = ['movies']
