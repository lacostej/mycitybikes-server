# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404, to_json_data
from mycitybikes import utils
from mycitybikes.models import *
from mycitybikes.forms import *
from google.appengine.ext import db
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
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
  station = get_object_or_404(BikeStation, id=int(stationId))
  if station.providerRef.cityRef != city:
    raise Http404
  doc = utils.object_to_xml(station)
  return HttpResponse(doc.toxml(), content_type="text/xml")
    

def stations_put(request, id_n):
  if request.method == "PUT":
    data = request.raw_post_data
    try:
      xmltree = ET.XML(data)
    except:
      raise HttpResponseBadRequest
    
    try:
      save_station_status(xmltree)
      return HttpResponse("OK")
    except InvalidXML, e:
      return HttpResponseBadRequest(e.message)
    except InvalidXMLNode, e:
      return HttpResponseBadRequest(e.message)
    except Exception, e: 
      return HttpResponse(e.message)
    return HttpResponse("ERRORX")
    
  else:
    return HttpResponse("ERROR")

  
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

#Status
def statuses_by_city_get(request, cityId):
  city = get_object_or_404(City, id=int(cityId))
  stations = itertools.chain(*[provider.bikestation_set for provider in city.provider_set])
  statuses = itertools.chain(*[station.bikestationstatus_set for station in stations])
  doc = utils.object_to_xml(statuses, "stationStatuses")
  return HttpResponse(doc.toxml(), content_type="text/xml")

def status_by_city_get(request, cityId, stationId):#ask about it
  city = get_object_or_404(City, id=int(cityId))
  station = get_object_or_404(BikeStation, id=int(stationId))
  if station.city != city:
    raise Http404
  status = station.bikestationstatus_set.get()
  doc = utils.object_to_xml(status)
  return HttpResponse(doc.toxml(), content_type="text/xml")
    

def save_station_status(xmltree):
#TODO make it works for single station  
  if xmltree.tag != 'stationAndstatuses':
    raise InvalidXML
  stations = []
  statuses = []
  for node in xmltree:
    if node.tag != 'stationAndStatus':
      raise InvalidXMLNode("Expected stationAndstatuses but got %s" % xmltree.tag)
    node = xmlnode2dict(node)
    station_form = BikeStationForm(node)
    status_form = StatusForm(node.get('stationStatus',{}))
    if not station_form.is_valid() or not status_form.is_valid():
      raise InvalidXMLNode(node)
    stations.append(station_form.get_model())
    statuses.append(status_form)
  db.put(stations)
  statuses = [status.get_model(station) for station, status in zip(stations, statuses)]
  db.put(statuses)
  
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
