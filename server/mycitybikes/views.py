# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404, to_json_data
from mycitybikes.models import *
from mycitybikes import utils
from xml.dom.minidom import Document
import logging
import itertools

#Station
def stations_get(request):
  doc = utils.object_to_xml(BikeStation.all(), "stations")
  return HttpResponse(doc.toxml(), content_type="text/xml")

def station_get(request, station_id):
  station = get_object_or_404(BikeStation, id=int(station_id))
  doc = utils.object_to_xml(station)
  return HttpResponse(doc.toxml(), content_type="text/xml")

def stations_by_city_get(request, city_id):    
  city = get_object_or_404(City, id=int(city_id))
  stations = itertools.chain(*[provider.bikestation_set for provider in city.provider_set])
  doc = utils.object_to_xml(stations, "stations")
  return HttpResponse(doc.toxml(), content_type="text/xml")

def station_by_city_get(request, cityId, stationId):
  city = get_object_or_404(City, id=int(cityId))  
  station = city.provider_set.get().get_by_id(int(stationId))
  if station:
    doc = utils.object_to_xml(station)
    return HttpResponse(doc.toxml(), content_type="text/xml")
  else:
    raise Http404

#City
def cities_get(request):
  doc = utils.object_to_xml(City.all(), "cities")
  return HttpResponse(doc.toxml(), content_type="text/xml")

def city_get(request, city_id):
  city = get_object_or_404(City, id=int(city_id))
  doc = utils.object_to_xml(city)
  return HttpResponse(doc.toxml(), content_type="text/xml")

#Provider

def providers_get(request):
  doc = utils.object_to_xml(Provider.all(), "providers")
  return HttpResponse(doc.toxml(), content_type="text/xml")

def provider_get(request, provider_id):
  provider = get_object_or_404(Provider.all(), id=int(provider_id))
  doc = utils.object_to_xml(provider)
  return HttpResponse(doc.toxml(), content_type="text/xml")

def providers_by_city_get(request, city_id):    
  city = get_object_or_404(City, id=int(city_id))
  doc = utils.object_to_xml(city.provider_set, "providers")
  return HttpResponse(doc.toxml(), content_type="text/xml")

"""
def city_get(request, cityId):
  city = City.get_by_id(int(cityId))
  logging.info(city.to_xml().toxml())
  return HttpResponse(city.to_xml().toxml(), content_type="text/xml")

def provider_stations_put(request, providerId):
  logging.info(request.raw_post_data)

  # FIXME we need to map name to id or introduce an externalId field

#    stations = BikeStation.from_xml(request.raw_post_data)
#    for station in stations:
#        station = BikeStation.get_by_id(station.key().id())

  return HttpResponse('')

def provider_stations_get(request, providerId):
  doc = Document()
  root = doc.createElement(u"stations")
  for station in BikeStation.all().filter("providerRef = ", providerId):
    root.appendChild(station.to_xml())
  doc.appendChild(root)
  return HttpResponse(doc.toxml(), content_type="text/xml")

def city_stations_get(request, cityId):
  doc = Document()
  root = doc.createElement(u"stations")
  for station in BikeStation.all():
    root.appendChild(station.to_xml())
  doc.appendChild(root)
  return HttpResponse(doc.toxml(), content_type="text/xml")

"""