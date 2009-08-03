# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from xml.dom.minidom import Document
from utils import model_to_dict, dict_to_xml, delete_keys, obj2dict, xmlnode2dict
from google.appengine.ext.db import djangoforms

from mycitybikes.forms import *
"""
class Base(db.Model):
  creationDateTime = db.DateTimeProperty(required=False, auto_now_add=True)
  updateDateTime = db.DateTimeProperty(required=False, auto_now=True)

class Positionable(Base):
  geoloc = db.GeoPtProperty(required=True)
"""


class InvalidXML(Exception):
  pass

class InvalidXMLNode(Exception):
  pass

class City(db.Model):
  name = db.StringProperty(required=True)
  country = db.StringProperty(required=True)
  externalId = db.StringProperty(required=True)
  geoloc = db.GeoPtProperty(required=True)
  creationDateTime = db.DateTimeProperty(required=False, auto_now_add=True)
  updateDateTime = db.DateTimeProperty(required=False, auto_now=True)

  def __unicode__(self):
    return '%s' % (self.name)

  def to_xml(self):
    extra = dict(id=self.key().id(),
                 latitude=self.geoloc.lat, 
                 longitude=self.geoloc.lon,
                 creationDateTime=unicode(self.updateDateTime.isoformat()+ "Z"),
                 updateDateTime=unicode(self.updateDateTime.isoformat() + "Z"))
    city = obj2dict(self, self.properties(), exclude=['geoloc'], extra= extra)
    city = dict_to_xml(city, "city")
    return city

class Provider(db.Model):
  shortName = db.StringProperty(required=True)
  fullName = db.StringProperty(required=True)
  cityRef = db.ReferenceProperty(City, required=True)
  locationsUpdated = db.DateTimeProperty(required=True)
  creationDateTime = db.DateTimeProperty(required=False, auto_now_add=True)
  updateDateTime = db.DateTimeProperty(required=False, auto_now=True)
  
  def __unicode__(self):
    return self.shortName

  @property
  def latitude(self):
    return self.cityRef.geoloc.lat

  @property
  def longitude(self):
    return self.cityRef.geoloc.lon
  
  def to_xml(self):
    extra = dict(id=self.key().id(),
                 latitude=self.geoloc.lat, 
                 longitude=self.geoloc.lon,
                 cityId=self.cityRef.key().id(),
                 creationDateTime=unicode(self.updateDateTime.isoformat()+ "Z"),
                 updateDateTime=unicode(self.updateDateTime.isoformat() + "Z"),
                 locationsUpdated=unicode(self.locationsUpdated.isoformat() + "Z"))
    provider = obj2dict(self, self.properties(), exclude=['cityRef','geoloc'], extra=extra)
    provider = dict_to_xml(provider, "provider")
    return provider

class BikeStation(db.Model):
  name = db.StringProperty(required=True)
  providerRef = db.ReferenceProperty(Provider, required=True)
  description = db.StringProperty(required=True)
  externalId = db.StringProperty(required=False) # Ask about it
  geoloc = db.GeoPtProperty(required=True)
  creationDateTime = db.DateTimeProperty(required=False, auto_now_add=True)
  updateDateTime = db.DateTimeProperty(required=False, auto_now=True)
  
  def __unicode__(self):
    return self.name
  
  @property
  def latitude(self):
    return self.providerRef.latitude

  @property
  def longitude(self):
    return self.providerRef.longitude

  @property
  def city(self):
    return self.providerRef.cityRef
  
  def to_xml(self):
    extra = dict(id=self.key().id(),
             latitude=self.geoloc.lat, 
             longitude=self.geoloc.lon,
             providerId=self.providerRef.key().id(),
             cityId=self.providerRef.cityRef.key().id(),
             creationDateTime=unicode(self.updateDateTime.isoformat()+ "Z"),
             updateDateTime=unicode(self.updateDateTime.isoformat() + "Z"))
    station = obj2dict(self, self.properties(), exclude=['providerRef', 'geoloc'], extra=extra)
    station = dict_to_xml(station, "station")
    return station
  
  @staticmethod
  def save_from_xml(xmltree):
    if xmltree.tag != 'stations':
      raise InvalidXML
    stations = []
    for node in xmltree:
      if node.tag == 'station':
        node = xmlnode2dict(node)
        #if not contains_keys(node, ["id","description","latitude","longitude"]):
        #  raise InvalidXMLNode
        form = BikeStationForm(node)
        if form.is_valid():
          stations.append(form.get_model())
        else:
          raise InvalidXMLNode
      else:
        raise InvalidXMLNode
    for station in stations:
      station.put()
  
      
      
      
class StationForm(djangoforms.ModelForm):
  class Meta:
    model = BikeStation
    exclude = ['creationDateTime', 'updateDateTime', 'geoloc']



  

class BikeStationStatus(db.Model):
  stationRef = db.ReferenceProperty(BikeStation, required=True)
  freeSlots = db.IntegerProperty(required=True)
  availableBikes = db.IntegerProperty(required=True)
  totalSlots = db.IntegerProperty(required=True)
  creationDateTime = db.DateTimeProperty(required=False, auto_now_add=True)
  updateDateTime = db.DateTimeProperty(required=False, auto_now=True)
  
  @property
  def city(self):
    return self.stationRef.providerRef.cityRef
  
  def __unicode__(self):
    return self.stationRef.name

  def to_xml(self):
    extra = dict(id=self.key().id(),
             stationRef=self.stationRef.key().id(),
             cityId=self.city.key().id(),
             stationId=self.stationRef.key().id(),
             creationDateTime=unicode(self.updateDateTime.isoformat()+ "Z"),
             updateDateTime=unicode(self.updateDateTime.isoformat() + "Z"))
    station = obj2dict(self, self.properties(), exclude=['stationRef', 'geoloc'], extra=extra)
    station = dict_to_xml(station, "stationStatus") #stationStatuses
    return station
  
  def xml2model(self, node):
    pass
  
"""
  def to_xml(self):
  station = model_to_dict(self)
  station['creationDateTime'] = unicode(self.updateDateTime.isoformat()+ "Z")
  station['updateDateTime'] = unicode(self.updateDateTime.isoformat() + "Z")
  station['providerId'] = self.providerRef.key().id()
  station['cityId'] = self.providerRef.cityRef.key().id()
  station['latitude'] = self.latitude
  station['longitude'] = self.longitude
  delete_keys(station, ['providerRef', 'geoloc'])
  station = dict_to_xml(station, "station")
  return station
  def __unicode__(self):
  return self.name
"""
