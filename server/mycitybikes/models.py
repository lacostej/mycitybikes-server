# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from xml.dom.minidom import Document

from utils import model_to_dict, dict_to_xml, delete_keys

class Base(polymodel.PolyModel):
    creationDateTime = db.DateTimeProperty(required=False)
    updateDateTime = db.DateTimeProperty(required=False)

class Positionable(Base):
    geoloc = db.GeoPtProperty(required=True)

class City(Positionable):
    name = db.StringProperty(required=True)
    country = db.StringProperty(required=True)

    def __unicode__(self):
        return '%s' % (self.name)

    def to_xml(self):
        city = model_to_dict(self)
        city['latitude'] = self.geoloc.lat
        city['longitude'] = self.geoloc.lon
        city['creationDateTime'] = unicode(self.updateDateTime.isoformat()+ "Z")
        city['updateDateTime'] = unicode(self.updateDateTime.isoformat() + "Z")
        delete_keys(city, ['geoloc'])
        city = dict_to_xml(city, "city")
        return city

class Provider(Base):
    shortName = db.StringProperty(required=True)
    fullName = db.StringProperty(required=True)
    cityRef = db.ReferenceProperty(City, required=True)
    locationsUpdated = db.DateTimeProperty(required=True)
    
    @property
    def latitude(self):
        return self.cityRef.geoloc.lat
    @property
    def longitude(self):
        return self.cityRef.geoloc.lon
    
    def to_xml(self):
        provider = model_to_dict(self)
        provider['creationDateTime'] = unicode(self.updateDateTime.isoformat()+ "Z")
        provider['updateDateTime'] = unicode(self.updateDateTime.isoformat() + "Z")
        provider['locationsUpdated'] = unicode(self.locationsUpdated.isoformat() + "Z")
        provider['cityId'] = self.cityRef.key().id()
        delete_keys(provider, ['cityRef','geoloc'])
        provider = dict_to_xml(provider, "provider")
        return provider
    def __unicode__(self):
        return self.shortName


class BikeStation(Positionable):
    name = db.StringProperty(required=True)
    providerRef = db.ReferenceProperty(Provider, required=True)
    description = db.StringProperty(required=True)
    
    @property
    def latitude(self):
        return self.providerRef.latitude
    @property
    def longitude(self):
        return self.providerRef.longitude
    
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