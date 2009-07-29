# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from mycitybikes.router import mapping
from mycitybikes.views import *

urlpatterns = patterns('',

    mapping(r'^stations/city/(?P<cityId>\d+)/all.xml$', 'city_stations',
            city_stations_get),

    mapping(r'^stations/provider/(?P<providerId>\d+)/all.xml$', 'provider_stations',
            provider_stations_get, None, provider_stations_put),

#    url(r'cities/$', cities_get),

    url(r'cities/(?P<cityId>\d+).xml$', city_get),
    
    url(r'cities.xml$', cities_get),

)
