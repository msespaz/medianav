
from south.db import db
from django.db import models
from movies.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VideoFile'
        db.create_table('movies_videofile', (
            ('id', orm['movies.VideoFile:id']),
            ('name', orm['movies.VideoFile:name']),
            ('movie', orm['movies.VideoFile:movie']),
            ('directory', orm['movies.VideoFile:directory']),
            ('ctime', orm['movies.VideoFile:ctime']),
            ('last_updated', orm['movies.VideoFile:last_updated']),
            ('file_size', orm['movies.VideoFile:file_size']),
            ('audio_bitrate', orm['movies.VideoFile:audio_bitrate']),
            ('audio_channels', orm['movies.VideoFile:audio_channels']),
            ('audio_codec', orm['movies.VideoFile:audio_codec']),
            ('audio_codec_id', orm['movies.VideoFile:audio_codec_id']),
            ('audio_format', orm['movies.VideoFile:audio_format']),
            ('audio_language', orm['movies.VideoFile:audio_language']),
            ('audio_resolution', orm['movies.VideoFile:audio_resolution']),
            ('audio_samplerate', orm['movies.VideoFile:audio_samplerate']),
            ('general_bitrate', orm['movies.VideoFile:general_bitrate']),
            ('general_codec', orm['movies.VideoFile:general_codec']),
            ('general_duration', orm['movies.VideoFile:general_duration']),
            ('general_format', orm['movies.VideoFile:general_format']),
            ('general_size', orm['movies.VideoFile:general_size']),
            ('video_bitrate', orm['movies.VideoFile:video_bitrate']),
            ('video_codec', orm['movies.VideoFile:video_codec']),
            ('video_codec_id', orm['movies.VideoFile:video_codec_id']),
            ('video_displayaspect', orm['movies.VideoFile:video_displayaspect']),
            ('video_pixelaspect', orm['movies.VideoFile:video_pixelaspect']),
            ('video_format', orm['movies.VideoFile:video_format']),
            ('video_width', orm['movies.VideoFile:video_width']),
            ('video_height', orm['movies.VideoFile:video_height']),
            ('video_scantype', orm['movies.VideoFile:video_scantype']),
        ))
        db.send_create_signal('movies', ['VideoFile'])
        
        # Adding model 'VideoDirectory'
        db.create_table('movies_videodirectory', (
            ('id', orm['movies.VideoDirectory:id']),
            ('name', orm['movies.VideoDirectory:name']),
            ('format', orm['movies.VideoDirectory:format']),
            ('movie', orm['movies.VideoDirectory:movie']),
            ('last_updated', orm['movies.VideoDirectory:last_updated']),
            ('ctime', orm['movies.VideoDirectory:ctime']),
            ('date_added', orm['movies.VideoDirectory:date_added']),
        ))
        db.send_create_signal('movies', ['VideoDirectory'])
        
        # Adding model 'MovieStatus'
        db.create_table('movies_moviestatus', (
            ('id', orm['movies.MovieStatus:id']),
            ('name', orm['movies.MovieStatus:name']),
        ))
        db.send_create_signal('movies', ['MovieStatus'])
        
        # Adding model 'Cast'
        db.create_table('movies_cast', (
            ('id', orm['movies.Cast:id']),
            ('person', orm['movies.Cast:person']),
            ('movie', orm['movies.Cast:movie']),
            ('role', orm['movies.Cast:role']),
            ('job', orm['movies.Cast:job']),
            ('bill_order', orm['movies.Cast:bill_order']),
        ))
        db.send_create_signal('movies', ['Cast'])
        
        # Adding model 'Movie'
        db.create_table('movies_movie', (
            ('id', orm['movies.Movie:id']),
            ('title', orm['movies.Movie:title']),
            ('imdb_id', orm['movies.Movie:imdb_id']),
            ('imdb_last_updated', orm['movies.Movie:imdb_last_updated']),
            ('imdb_long_title', orm['movies.Movie:imdb_long_title']),
            ('canon_title', orm['movies.Movie:canon_title']),
            ('imdb_canon_long_title', orm['movies.Movie:imdb_canon_long_title']),
            ('year', orm['movies.Movie:year']),
            ('imdb_kind', orm['movies.Movie:imdb_kind']),
            ('imdb_index', orm['movies.Movie:imdb_index']),
            ('imdb_cover_url', orm['movies.Movie:imdb_cover_url']),
            ('plot', orm['movies.Movie:plot']),
            ('plot_outline', orm['movies.Movie:plot_outline']),
            ('imdb_rating', orm['movies.Movie:imdb_rating']),
            ('imdb_votes', orm['movies.Movie:imdb_votes']),
            ('runtime', orm['movies.Movie:runtime']),
            ('mpaa', orm['movies.Movie:mpaa']),
            ('status', orm['movies.Movie:status']),
            ('watched', orm['movies.Movie:watched']),
            ('trailer_url', orm['movies.Movie:trailer_url']),
            ('moviedb_id', orm['movies.Movie:moviedb_id']),
            ('moviedb_rating', orm['movies.Movie:moviedb_rating']),
            ('moviedb_url', orm['movies.Movie:moviedb_url']),
            ('moviedb_poster_url', orm['movies.Movie:moviedb_poster_url']),
            ('moviedb_backdrop_url', orm['movies.Movie:moviedb_backdrop_url']),
            ('moviedb_last_updated', orm['movies.Movie:moviedb_last_updated']),
        ))
        db.send_create_signal('movies', ['Movie'])
        
        # Adding model 'Genre'
        db.create_table('movies_genre', (
            ('id', orm['movies.Genre:id']),
            ('name', orm['movies.Genre:name']),
        ))
        db.send_create_signal('movies', ['Genre'])
        
        # Adding model 'Person'
        db.create_table('movies_person', (
            ('id', orm['movies.Person:id']),
            ('name', orm['movies.Person:name']),
            ('imdb_id', orm['movies.Person:imdb_id']),
        ))
        db.send_create_signal('movies', ['Person'])
        
        # Adding model 'Language'
        db.create_table('movies_language', (
            ('id', orm['movies.Language:id']),
            ('name', orm['movies.Language:name']),
        ))
        db.send_create_signal('movies', ['Language'])
        
        # Adding model 'VideoFormat'
        db.create_table('movies_videoformat', (
            ('id', orm['movies.VideoFormat:id']),
            ('name', orm['movies.VideoFormat:name']),
        ))
        db.send_create_signal('movies', ['VideoFormat'])
        
        # Adding model 'Company'
        db.create_table('movies_company', (
            ('id', orm['movies.Company:id']),
            ('name', orm['movies.Company:name']),
            ('imdb_id', orm['movies.Company:imdb_id']),
        ))
        db.send_create_signal('movies', ['Company'])
        
        # Adding model 'Certificate'
        db.create_table('movies_certificate', (
            ('id', orm['movies.Certificate:id']),
            ('name', orm['movies.Certificate:name']),
        ))
        db.send_create_signal('movies', ['Certificate'])
        
        # Adding model 'Country'
        db.create_table('movies_country', (
            ('id', orm['movies.Country:id']),
            ('name', orm['movies.Country:name']),
        ))
        db.send_create_signal('movies', ['Country'])
        
        # Adding ManyToManyField 'Movie.genres'
        db.create_table('movies_movie_genres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm.Movie, null=False)),
            ('genre', models.ForeignKey(orm.Genre, null=False))
        ))
        
        # Adding ManyToManyField 'Movie.certificates'
        db.create_table('movies_movie_certificates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm.Movie, null=False)),
            ('certificate', models.ForeignKey(orm.Certificate, null=False))
        ))
        
        # Adding ManyToManyField 'Movie.production_companies'
        db.create_table('movies_movie_production_companies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm.Movie, null=False)),
            ('company', models.ForeignKey(orm.Company, null=False))
        ))
        
        # Adding ManyToManyField 'Movie.languages'
        db.create_table('movies_movie_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm.Movie, null=False)),
            ('language', models.ForeignKey(orm.Language, null=False))
        ))
        
        # Adding ManyToManyField 'Movie.countries'
        db.create_table('movies_movie_countries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movie', models.ForeignKey(orm.Movie, null=False)),
            ('country', models.ForeignKey(orm.Country, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VideoFile'
        db.delete_table('movies_videofile')
        
        # Deleting model 'VideoDirectory'
        db.delete_table('movies_videodirectory')
        
        # Deleting model 'MovieStatus'
        db.delete_table('movies_moviestatus')
        
        # Deleting model 'Cast'
        db.delete_table('movies_cast')
        
        # Deleting model 'Movie'
        db.delete_table('movies_movie')
        
        # Deleting model 'Genre'
        db.delete_table('movies_genre')
        
        # Deleting model 'Person'
        db.delete_table('movies_person')
        
        # Deleting model 'Language'
        db.delete_table('movies_language')
        
        # Deleting model 'VideoFormat'
        db.delete_table('movies_videoformat')
        
        # Deleting model 'Company'
        db.delete_table('movies_company')
        
        # Deleting model 'Certificate'
        db.delete_table('movies_certificate')
        
        # Deleting model 'Country'
        db.delete_table('movies_country')
        
        # Dropping ManyToManyField 'Movie.genres'
        db.delete_table('movies_movie_genres')
        
        # Dropping ManyToManyField 'Movie.certificates'
        db.delete_table('movies_movie_certificates')
        
        # Dropping ManyToManyField 'Movie.production_companies'
        db.delete_table('movies_movie_production_companies')
        
        # Dropping ManyToManyField 'Movie.languages'
        db.delete_table('movies_movie_languages')
        
        # Dropping ManyToManyField 'Movie.countries'
        db.delete_table('movies_movie_countries')
        
    
    
    models = {
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
