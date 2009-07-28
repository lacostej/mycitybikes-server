# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('mycitybikes.views',
    (r'cities/$', 'list_cities'),
    
    (r'cities.xml$', 'list_cities'),
)
