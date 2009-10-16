from django.conf.urls.defaults import *
# For serving static pages
from django.views import static

# Django authentication
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^medianav/', include('medianav.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^medianav/admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^medianav/admin/(.*)', admin.site.root),

    # Custom app views
    (r'^medianav/tv/', include('tv.urls')),
    (r'^medianav/movies/', include('movies.urls')),
    (r'^medianav/pch/', include('pch.urls')),

    # Authentication views
    (r'^medianav/accounts/login/$', login),
    (r'^medianav/accounts/logout/$', logout),

    # Media - This should not be served from django, but this is useful
    # for a development server
    (r'^medianav/media/(?P<path>.*)$', static.serve, {'document_root': 'media', 'show_indexes': True}),
    
    # Default page
    (r'^medianav/', include('mnav.urls')),

)
