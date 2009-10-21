
from south.db import db
from django.db import models
from mnav.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VideoFile'
        db.create_table('mnav_videofile', (
            ('id', orm['mnav.VideoFile:id']),
            ('name', orm['mnav.VideoFile:name']),
            ('ctime', orm['mnav.VideoFile:ctime']),
            ('last_updated', orm['mnav.VideoFile:last_updated']),
            ('file_size', orm['mnav.VideoFile:file_size']),
            ('audio_bitrate', orm['mnav.VideoFile:audio_bitrate']),
            ('audio_channels', orm['mnav.VideoFile:audio_channels']),
            ('audio_codec', orm['mnav.VideoFile:audio_codec']),
            ('audio_codec_id', orm['mnav.VideoFile:audio_codec_id']),
            ('audio_format', orm['mnav.VideoFile:audio_format']),
            ('audio_language', orm['mnav.VideoFile:audio_language']),
            ('audio_resolution', orm['mnav.VideoFile:audio_resolution']),
            ('audio_samplerate', orm['mnav.VideoFile:audio_samplerate']),
            ('general_bitrate', orm['mnav.VideoFile:general_bitrate']),
            ('general_codec', orm['mnav.VideoFile:general_codec']),
            ('general_duration', orm['mnav.VideoFile:general_duration']),
            ('general_format', orm['mnav.VideoFile:general_format']),
            ('general_size', orm['mnav.VideoFile:general_size']),
            ('video_bitrate', orm['mnav.VideoFile:video_bitrate']),
            ('video_codec', orm['mnav.VideoFile:video_codec']),
            ('video_codec_id', orm['mnav.VideoFile:video_codec_id']),
            ('video_displayaspect', orm['mnav.VideoFile:video_displayaspect']),
            ('video_pixelaspect', orm['mnav.VideoFile:video_pixelaspect']),
            ('video_format', orm['mnav.VideoFile:video_format']),
            ('video_width', orm['mnav.VideoFile:video_width']),
            ('video_height', orm['mnav.VideoFile:video_height']),
            ('video_scantype', orm['mnav.VideoFile:video_scantype']),
        ))
        db.send_create_signal('mnav', ['VideoFile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VideoFile'
        db.delete_table('mnav_videofile')
        
    
    
    models = {
        'mnav.videofile': {
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
        }
    }
    
    complete_apps = ['mnav']
