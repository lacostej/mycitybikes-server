# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404

from mycitybikes.models import *
from xml.dom.minidom import Document

import logging

def list_cities(request):
  doc = Document()
  cities = doc.createElement(u"cities")
  for city in City.all():
    cities.appendChild(city.to_xml())
  doc.appendChild(cities)
  return HttpResponse(doc.toxml(), content_type="text/xml")

def list_stations(request):
  doc = Document()
  stations = doc.createElement(u"stations")
  for station in BikeStation.all():
    stations.appendChild(station.to_xml())
  doc.appendChild(stations)
  return HttpResponse(doc.toxml(), content_type="text/xml")


def cities_get(request):
  doc = Document()
  cities = doc.createElement(u"cities")
  for city in City.all():
    cities.appendChild(city.to_xml())
  doc.appendChild(cities)
  return HttpResponse(doc.toxml(), content_type="text/xml")


def get_city(request, city_id):
  #return HttpResponse("FDSAFDS")
  city = get_object_or_404(City, id=int(city_id))
  doc = Document()
  doc.appendChild(city.to_xml())
  return HttpResponse(doc.toxml(), content_type="text/xml")

def get_station(request, station_id):
  station = get_object_or_404(BikeStation, id=int(station_id))
  doc = Document()
  doc.appendChild(station.to_xml())
  return HttpResponse(doc.toxml(), content_type="text/xml")


def list_providers_by_city(request, city_id):    
  city = get_object_or_404(City, id=int(city_id))
  doc = Document()
  providers = doc.createElement(u"providers")
  for provider in city.provider_set:
    providers.appendChild(provider.to_xml())    
  doc.appendChild(providers)
  return HttpResponse(doc.toxml(), content_type="text/xml")

def list_stations_by_city(request, city_id):    
  city = get_object_or_404(City, id=int(city_id))
  doc = Document()
  stations = doc.createElement(u"stations")
  for provider in city.provider_set:
    for station in provider.bikestation_set:
      stations.appendChild(station.to_xml())    
  doc.appendChild(stations)
  return HttpResponse(doc.toxml(), content_type="text/xml")


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

