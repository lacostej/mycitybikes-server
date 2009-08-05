# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from ragendja.dbutils import get_object_or_404, to_json_data
from mycitybikes.models import *
from mycitybikes import utils
from google.appengine.ext import db
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
import logging
import itertools
class BikeStationForm(forms.Form):
  providerId = forms.IntegerField(min_value=0)
  name = forms.CharField(required=False, )
  description = forms.CharField(required=False)
  latitude = forms.FloatField()
  longitude = forms.FloatField()
  #updateDateTime = forms.RegexField() # TODO write the regex to match time isoformat
  def get_geoloc(self):
    data = self.cleaned_data
    return db.GeoPt(data['latitude'], data['longitude'])

  def clean_providerId(self):
    providerId = self.cleaned_data['providerId']
    provider = Provider.get_by_id(providerId)
    if not provider:
      raise  forms.ValidationError("Provider ID doesn't exists")
    self.cleaned_data['provider'] = provider
    
  def get_model(self):
    data = self.cleaned_data
    return BikeStation(providerRef=data['provider'],
                       name=data['description'],
                       description=data['description'],
                       geoloc=self.get_geoloc(),
                       externalId="111")
  
class StatusForm(forms.Form):
  online = forms.IntegerField(required=True, min_value=0)
  availableBikes = forms.IntegerField(required=False, min_value=0)
  freeSlots = forms.IntegerField(required=False, min_value=0)
  totalSlots = forms.IntegerField(required=False, min_value=0)
  
  def get_model(self,station):
    data = self.cleaned_data
    return BikeStationStatus(stationRef=station,
                             availableBikes=data['availableBikes'],
                             freeSlots=data['freeSlots'], totalSlots=data['totalSlots'])

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
  if station.providerRef.cityRef == city:
    doc = utils.object_to_xml(station)
    return HttpResponse(doc.toxml(), content_type="text/xml")
  else:
    raise Http404

def stations_put(request, id_n):
  if request.method == "PUT":
    data = request.raw_post_data
    try:
      xmltree = ET.XML(data)
    except:
      raise HttpResponseBadRequest
    try:
      #BikeStation.save_from_xml(xmltree)
      save_station_status(xmltree)
    except InvalidXML:
      return HttpResponseBadRequest("Invalid XML")
    except InvalidXMLNode:
      return HttpResponseBadRequest("Invalid XML Node")
    except Exception, e: 
      return HttpResponse(e)
    return HttpResponse("OK")
  else:
    return HttpResponse("ERROR")
    #nodes = [utils.xmlnode2dict(node) for node in tree]
# logging.info(data)
# logging.info(dir(request))
  
  
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
  if station.city == city:
    status = station.bikestationstatus_set.get()
    doc = utils.object_to_xml(status)
    return HttpResponse(doc.toxml(), content_type="text/xml")
  else:
    raise Http404
  


def save_station_status(xmltree):
  if xmltree.tag != 'stationAndstatuses':
    raise InvalidXML
  stations_statuses = []
  for node in xmltree:
    if node.tag == 'stationAndStatus':
      node = xmlnode2dict(node)
      #node['providerId'] = 4 # MAGIC NUMBER
      station_form = BikeStationForm(node)
      status_form = StatusForm(node.get('stationStatus',{}))
      if station_form.is_valid() and status_form.is_valid():
        #if node.has_key('stationStatus'):
        station = station_form.get_model()
        stations_statuses.append((station, status_form))
      else:
        raise InvalidXMLNode()
    else:
      raise InvalidXMLNode()
  for station, status in stations_statuses:
    station.put()
    status = status.get_model(station)
    status.save()
  
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
