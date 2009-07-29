# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from xml.dom.minidom import Document

class Base(polymodel.PolyModel):
    creationDatetime = db.DateTimeProperty(required=False)
    updateDatetime = db.DateTimeProperty(required=False)

class Positionable(Base):
    geoloc = db.GeoPtProperty(required=True)

class City(Positionable):
    name = db.StringProperty(required=True)
    country = db.StringProperty(required=True)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    def to_xml(self):
        doc = Document()
        city = doc.createElement("city")
        id_ = doc.createElement(u"id")
        id_.appendChild(doc.createTextNode(unicode(self.key().id())))
        name = doc.createElement(u"name")
        name.appendChild(doc.createTextNode(unicode(self.name)))
        country = doc.createElement(u"country")
        country.appendChild(doc.createTextNode(unicode(self.country)))
        latitude = doc.createElement(u"latitude")
        latitude.appendChild(doc.createTextNode(unicode(self.geoloc.lat)))
        longitude = doc.createElement(u"longitude")
        longitude.appendChild(doc.createTextNode(unicode(self.geoloc.lon)))
        creationDatetime = doc.createElement(u"creationDateTime")
        creationDatetime.appendChild(doc.createTextNode(unicode(self.updateDatetime.isoformat()+ "Z")))
        updateDatetime = doc.createElement(u"updateDateTime")
        updateDatetime.appendChild(doc.createTextNode(unicode(self.updateDatetime.isoformat() + "Z")))
        city.appendChild(id_)
        city.appendChild(name)
        city.appendChild(country)
        city.appendChild(latitude)
        city.appendChild(longitude)
        city.appendChild(creationDatetime)
        city.appendChild(updateDatetime)
        return city

class Provider(Base):
    shortName = db.StringProperty(required=True)
    fullName = db.StringProperty(required=True)
    cityRef = db.ReferenceProperty(City, required=True)

class BikeStation(Positionable):
    name = db.StringProperty(required=True)
    providerRef = db.ReferenceProperty(Provider, required=True)
    description = db.StringProperty(required=True)
    def to_xml(self):
        station = model_to_dict(self)
        station['creationDatetime'] = unicode(self.updateDatetime.isoformat()+ "Z")
        station['updateDatetime'] = unicode(self.updateDatetime.isoformat() + "Z")
        station['providerRef'] = self.providerRef.key().id()
        station = dict_to_xml(station, "station")
        return station
