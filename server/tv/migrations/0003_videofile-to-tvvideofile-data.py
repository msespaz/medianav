
from south.db import db
from django.db import models
from tv.models import *

class Migration:
    # During a dry the ORM cannot be accessed
    # since this whole migration is a data migration
    # disable dry runs
    no_dry_run = True

    def forwards(self, orm):
        for o in orm['tv.VideoFile'].objects.all():
            new = orm.TVVideoFile(show = o.show)
            new.basevideofile_ptr = orm['mnav.BaseVideoFile'].objects.create()
            new.basevideofile_ptr.name = o.name
            new.basevideofile_ptr.save()
            new.save()
            new.episodes = o.episodes.all()
    
    def backwards(self, orm):
        for o in orm['tv.TVVideoFile'].objects.all():
            new = orm.VideoFile(show = o.show)
            new.name = o.basevideofile_ptr.name
            new.save()
            new.episodes = o.episodes.all()
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'tv.alternateshowname': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Show']", 'blank': 'True'})
        },
        'tv.episode': {
            'director': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'episode_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_aired': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'guest_stars': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'overview': ('django.db.models.fields.CharField', [], {'max_length': '4024', 'blank': 'True'}),
            'production_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'season_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seen_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Show']", 'blank': 'True'}),
            'tvdb_episodeid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tvdb_image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tvdb_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'tvdb_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tvdb_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'writer': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'tv.show': {
            'airs_day': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'airs_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'content_rating': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'fav_of': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'first_aired': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'overview': ('django.db.models.fields.CharField', [], {'max_length': '4024', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'tvdb_banner_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tvdb_fanart_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tvdb_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'tvdb_last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tvdb_poster_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tvdb_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tvdb_showid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'tv.tvvideofile': {
            'basevideofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mnav.BaseVideoFile']", 'unique': 'True', 'primary_key': 'True'}),
            'episodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tv.Episode']"}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Show']", 'null': 'True', 'blank': 'True'})
        },
        'tv.videofile': {
            'episodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tv.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tv.Show']", 'null': 'True', 'blank': 'True'})
        },
        'tv.videofilepattern': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            're': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }
    
    complete_apps = ['tv']
