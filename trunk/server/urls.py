from django.conf.urls.defaults import *

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
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    # Custom app views
    (r'^/*tv/', include('tv.urls')),
    (r'^/*movies/', include('movies.urls')),

    # Authentication views
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/profile/$', "tv.views.shows_list"),
)
