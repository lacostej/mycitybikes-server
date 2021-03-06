# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from mycitybikes.router import mapping
from mycitybikes.views import *

# FIXME this is invalid and we respond to unwanted urls.
# e.g. invalidcities/ triggers cities/

urlpatterns = patterns('mycitybikes.views',
#GET
    (r'cities/all\.xml$', 'cities_get'),
# these 2 are deprecated. Replaced by cities/all.xml for consistency
    (r'cities/$', 'cities_get'),
    (r'cities\.xml$', 'cities_get'),

    (r'cities/(\d+)\.xml$', 'city_get'),
# deprecated. Replaced by stations/all.xml for consistency
    (r'stations/$', 'stations_get'),
    (r'stations/all\.xml$', 'stations_get'),
    (r'stations/(\d+)\.xml$', 'station_get'),
    (r'stations/city/(\d+)/all\.xml', 'stations_by_city_get'),
    (r'stations/city/(?P<cityId>\d+)/(?P<stationId>\d+)\.xml', 'station_by_city_get'),
    (r'providers/all\.xml', 'providers_get'),
    (r'providers/(?P<provider_id>\d+)\.xml', 'provider_get'),
    (r'providers/city/(\d+)/all\.xml', 'providers_by_city_get'),
    
    (r'stationStatuses/city/(?P<cityId>\d+)/all\.xml', 'statuses_by_city_get'),
    
    (r'stationsStatuses/city/(?P<cityId>\d+)/all\.xml', 'statuses_by_city_get'),
    (r'stationsStatuses/provider/(?P<providerId>\d+)/all.xml', 'statuses_by_provider_get'),
    (r'stationStatuses/city/(?P<cityId>\d+)/(?P<stationId>\d+)\.xml', 'status_by_station_get'),    
    
    #(r'stationsStatuses/city/(?P<cityId>\d+)/(?P<status>\d+)\.xml', 'status_get'),

# PUT
    (r'stationAndStatuses/provider/(?P<providerId>\d+)/all\.xml', 'stations_put'),
)
