from django.conf.urls.defaults import *

urlpatterns = patterns('pch.views',
    (r'^$', 'popcornhour_home'),
    (r'^all/(?P<page_number>\d+)/$', 'popcornhour_all'),
    (r'^detail/(?P<movie_id>\d+)/$', 'popcornhour_detail'),
)
