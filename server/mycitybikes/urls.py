# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from mycitybikes.router import mapping
from mycitybikes.views import *

urlpatterns = patterns('',

    mapping(r'^stations/provider/(?P<providerId>\d+)/all.xml$', 'provider_stations',
            provider_stations_get, None, provider_stations_put),

    url(r'cities/$', cities_get),
    
    url(r'cities.xml$', cities_get),

)
