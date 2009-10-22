
from south.db import db
from django.db import models
from movies.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting model 'videofile'
        db.delete_table('movies_videofile')
        
    
    
    def backwards(self, orm):
        
        # Adding model 'videofile'
        db.create_table('movies_videofile', (
            ('last_updated', orm['movies.videofile:last_updated']),
            ('audio_samplerate', orm['movies.videofile:audio_samplerate']),
            ('audio_language', orm['movies.videofile:audio_language']),
            ('audio_codec', orm['movies.videofile:audio_codec']),
            ('file_size', orm['movies.videofile:file_size']),
            ('id', orm['movies.videofile:id']),
            ('video_scantype', orm['movies.videofile:video_scantype']),
            ('general_size', orm['movies.videofile:general_size']),
            ('movie', orm['movies.videofile:movie']),
            ('video_height', orm['movies.videofile:video_height']),
            ('audio_codec_id', orm['movies.videofile:audio_codec_id']),
            ('audio_channels', orm['movies.videofile:audio_channels']),
            ('audio_format', orm['movies.videofile:audio_format']),
            ('audio_resolution', orm['movies.videofile:audio_resolution']),
            ('video_format', orm['movies.videofile:video_format']),
            ('audio_bitrate', orm['movies.videofile:audio_bitrate']),
            ('general_format', orm['movies.videofile:general_format']),
            ('video_width', orm['movies.videofile:video_width']),
            ('ctime', orm['movies.videofile:ctime']),
            ('name', orm['movies.videofile:name']),
            ('general_bitrate', orm['movies.videofile:general_bitrate']),
            ('video_bitrate', orm['movies.videofile:video_bitrate']),
            ('video_pixelaspect', orm['movies.videofile:video_pixelaspect']),
            ('video_displayaspect', orm['movies.videofile:video_displayaspect']),
            ('directory', orm['movies.videofile:directory']),
            ('video_codec', orm['movies.videofile:video_codec']),
            ('video_codec_id', orm['movies.videofile:video_codec_id']),
            ('general_codec', orm['movies.videofile:general_codec']),
            ('general_duration', orm['movies.videofile:general_duration']),
        ))
        db.send_create_signal('movies', ['videofile'])
        
    
    
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
        'movies.videoformat': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }
    
    complete_apps = ['movies']
