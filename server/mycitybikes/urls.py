# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from mycitybikes.router import mapping
from mycitybikes.views import *


urlpatterns = patterns('mycitybikes.views',
    (r'cities/$', 'cities_get'),
    (r'cities\.xml$', 'cities_get'),
    (r'cities/(\d+)\.xml$', 'city_get'),
    (r'stations/$', 'stations_get'),
    (r'stations/(\d+)\.xml$', 'station_get'),
    (r'stations/city/(\d+)/all\.xml', 'stations_by_city_get'),
    (r'stations/city/(?P<cityId>\d+)/(?P<stationId>\d+)\.xml', 'station_by_city_get'),
    (r'providers/city/(\d+)/all\.xml', 'providers_by_city_get'),
    (r'stationStatuses/city/(?P<cityId>\d+)/all\.xml', 'statuses_by_city_get'),
    (r'stationStatuses/city/(?P<cityId>\d+)/(?P<stationId>\d+)\.xml', 'status_by_city_get'),
)

"""
urlpatterns += patterns('',
    mapping(r'^stations/city/(?P<cityId>\d+)/all.xml$', 'city_stations',
            city_stations_get),
    mapping(r'^stations/provider/(?P<providerId>\d+)/all.xml$', 'provider_stations',
            provider_stations_get, None, provider_stations_put),
#    url(r'cities/$', cities_get),
    url(r'cities/(?P<cityId>\d+).xml$', city_get),
    
    url(r'cities.xml$', cities_get),

)

"""