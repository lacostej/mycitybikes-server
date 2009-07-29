# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from mycitybikes.router import mapping
from mycitybikes.views import *


urlpatterns = patterns('mycitybikes.views',
    (r'cities/$', 'list_cities'),
    (r'cities\.xml$', 'list_cities'),
    (r'cities/(\d+)\.xml$', 'get_city'),
    (r'stations/$', 'list_stations'),
    (r'stations/(\d+)\.xml$', 'get_station'),
    (r'providers/city/(\d+)/all\.xml', 'list_providers_by_city'),
    (r'stations/city/(\d+)/all\.xml', 'list_stations_by_city'),
    
)


urlpatterns += patterns('',
    mapping(r'^stations/city/(?P<cityId>\d+)/all.xml$', 'city_stations',
            city_stations_get),
    mapping(r'^stations/provider/(?P<providerId>\d+)/all.xml$', 'provider_stations',
            provider_stations_get, None, provider_stations_put),
#    url(r'cities/$', cities_get),
    url(r'cities/(?P<cityId>\d+).xml$', city_get),
    
    url(r'cities.xml$', cities_get),

)