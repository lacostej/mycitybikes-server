# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('mycitybikes.views',
    (r'cities/$', 'list_cities'),
    (r'cities\.xml$', 'list_cities'),
    (r'cities/(\d+)\.xml$', 'get_city'),
    (r'stations/$', 'list_stations'),
    (r'stations/(\d+)\.xml$', 'get_station'),
    (r'providers/city/(\d+)/all\.xml', 'list_providers_by_city'),
    (r'stations/city/(\d+)/all\.xml', 'list_stations_by_city'),
    
    #(r'cities\.xml$', 'list_cities'),
)