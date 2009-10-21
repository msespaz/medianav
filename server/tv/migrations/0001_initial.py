
from south.db import db
from django.db import models
from tv.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VideoFilePattern'
        db.create_table('tv_videofilepattern', (
            ('id', orm['tv.VideoFilePattern:id']),
            ('re', orm['tv.VideoFilePattern:re']),
            ('priority', orm['tv.VideoFilePattern:priority']),
            ('description', orm['tv.VideoFilePattern:description']),
        ))
        db.send_create_signal('tv', ['VideoFilePattern'])
        
        # Adding model 'AlternateShowName'
        db.create_table('tv_alternateshowname', (
            ('id', orm['tv.AlternateShowName:id']),
            ('name', orm['tv.AlternateShowName:name']),
            ('show', orm['tv.AlternateShowName:show']),
            ('priority', orm['tv.AlternateShowName:priority']),
        ))
        db.send_create_signal('tv', ['AlternateShowName'])
        
        # Adding model 'VideoFile'
        db.create_table('tv_videofile', (
            ('id', orm['tv.VideoFile:id']),
            ('name', orm['tv.VideoFile:name']),
            ('show', orm['tv.VideoFile:show']),
        ))
        db.send_create_signal('tv', ['VideoFile'])
        
        # Adding model 'Show'
        db.create_table('tv_show', (
            ('id', orm['tv.Show:id']),
            ('name', orm['tv.Show:name']),
            ('overview', orm['tv.Show:overview']),
            ('genre', orm['tv.Show:genre']),
            ('network', orm['tv.Show:network']),
            ('content_rating', orm['tv.Show:content_rating']),
            ('runtime', orm['tv.Show:runtime']),
            ('status', orm['tv.Show:status']),
            ('first_aired', orm['tv.Show:first_aired']),
            ('airs_day', orm['tv.Show:airs_day']),
            ('airs_time', orm['tv.Show:airs_time']),
            ('tvdb_language', orm['tv.Show:tvdb_language']),
            ('tvdb_showid', orm['tv.Show:tvdb_showid']),
            ('tvdb_rating', orm['tv.Show:tvdb_rating']),
            ('tvdb_banner_url', orm['tv.Show:tvdb_banner_url']),
            ('tvdb_poster_url', orm['tv.Show:tvdb_poster_url']),
            ('tvdb_fanart_url', orm['tv.Show:tvdb_fanart_url']),
            ('tvdb_last_updated', orm['tv.Show:tvdb_last_updated']),
        ))
        db.send_create_signal('tv', ['Show'])
        
        # Adding model 'Episode'
        db.create_table('tv_episode', (
            ('id', orm['tv.Episode:id']),
            ('name', orm['tv.Episode:name']),
            ('overview', orm['tv.Episode:overview']),
            ('season_number', orm['tv.Episode:season_number']),
            ('episode_number', orm['tv.Episode:episode_number']),
            ('director', orm['tv.Episode:director']),
            ('guest_stars', orm['tv.Episode:guest_stars']),
            ('production_code', orm['tv.Episode:production_code']),
            ('writer', orm['tv.Episode:writer']),
            ('show', orm['tv.Episode:show']),
            ('first_aired', orm['tv.Episode:first_aired']),
            ('tvdb_episodeid', orm['tv.Episode:tvdb_episodeid']),
            ('tvdb_language', orm['tv.Episode:tvdb_language']),
            ('tvdb_rating', orm['tv.Episode:tvdb_rating']),
            ('tvdb_image', orm['tv.Episode:tvdb_image']),
            ('tvdb_last_updated', orm['tv.Episode:tvdb_last_updated']),
        ))
        db.send_create_signal('tv', ['Episode'])
        
        # Adding ManyToManyField 'VideoFile.episodes'
        db.create_table('tv_videofile_episodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videofile', models.ForeignKey(orm.VideoFile, null=False)),
            ('episode', models.ForeignKey(orm.Episode, null=False))
        ))
        
        # Adding ManyToManyField 'Episode.seen_by'
        db.create_table('tv_episode_seen_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('episode', models.ForeignKey(orm.Episode, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'Show.fav_of'
        db.create_table('tv_show_fav_of', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('show', models.ForeignKey(orm.Show, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VideoFilePattern'
        db.delete_table('tv_videofilepattern')
        
        # Deleting model 'AlternateShowName'
        db.delete_table('tv_alternateshowname')
        
        # Deleting model 'VideoFile'
        db.delete_table('tv_videofile')
        
        # Deleting model 'Show'
        db.delete_table('tv_show')
        
        # Deleting model 'Episode'
        db.delete_table('tv_episode')
        
        # Dropping ManyToManyField 'VideoFile.episodes'
        db.delete_table('tv_videofile_episodes')
        
        # Dropping ManyToManyField 'Episode.seen_by'
        db.delete_table('tv_episode_seen_by')
        
        # Dropping ManyToManyField 'Show.fav_of'
        db.delete_table('tv_show_fav_of')
        
    
    
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
