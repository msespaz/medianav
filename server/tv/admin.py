from tv.models import *
from django.contrib import admin

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('show', 'season_number', 'episode_number', 'name')
    list_filter = ['show', 'season_number']
    search_fields = ['name', 'show__name']

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'runtime', 'status', 'first_aired')
    list_filter = ['genre', 'runtime', 'status']
    search_fields = ['name']

class AlternateShowNameAdmin(admin.ModelAdmin):
    list_display = ('show', 'name', 'priority')

class VideoFileAdmin(admin.ModelAdmin):
    list_display = ('show', 'name',)
    list_filter = ['show']
    search_fields = ['name',]

admin.site.register(Show, ShowAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(VideoFile, VideoFileAdmin)
admin.site.register(VideoFilePattern)
admin.site.register(AlternateShowName, AlternateShowNameAdmin)
