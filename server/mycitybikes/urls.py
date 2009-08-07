# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from mycitybikes.router import mapping
from mycitybikes.views import *

urlpatterns = patterns('mycitybikes.views',
#GET
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
# PUT
    (r'stationAndStatuses/provider/(?P<providerId>\d+)/all\.xml', 'stations_put'),
)