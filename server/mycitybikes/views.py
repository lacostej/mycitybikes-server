# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from mycitybikes.models import *
from xml.dom.minidom import Document

import logging

def cities_get(request):
    logging.info("*** list_cities")
    doc = Document()
    cities = doc.createElement(u"cities")
    for city in City.all():
        cities.appendChild(city.to_xml())
    doc.appendChild(cities)
    return HttpResponse(doc.toxml(), content_type="text/xml")

def provider_stations_put(request, providerId):
    logging.info("**** PUT ")
    return HttpResponse('')

def provider_stations_get(request, providerId):
    logging.info("**** GET ")
    return HttpResponse('')



