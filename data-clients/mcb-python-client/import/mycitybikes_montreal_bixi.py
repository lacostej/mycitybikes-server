#!/usr/bin/python
# mycitybikes_montreal_bixi.py

from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO
from xml.dom.minidom import Document
from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB

#MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")
MyCityBikes.setServerRoot("http://localhost:9000")

# comment this out to test communication to the stubs
#MyCityBikes.enableMocks()
def dict_to_xml(dct, node_name):
  doc = Document()
  node = doc.createElement(unicode(node_name, 'utf-8'))
  for k,v in dct.items():
    if isinstance(v,dict):
      e = dict_to_xml(v, k)
    else:
      e = doc.createElement(unicode(k))
      e.appendChild(doc.createTextNode(unicode(v)))
    node.appendChild(e)
  return node

def xmlnode2dict(node):
  result = {}
  for subnode in node:
    children = subnode.getchildren()
    if children:
      result[subnode.tag] = xmlnode2dict(subnode)
    else:
      result[subnode.tag] = subnode.text
  return result

def dict_from_keys(dct, dictkeys):
  result = {}
  for newkey, oldkey in dictkeys.iteritems():
    result[newkey] = dct.get(oldkey, '')
  return result

print "Starting Montreal,Bixi synchronization"
class StationAndStatus:
  def __init__(self, data):
    self.data = data
  def to_xml(self):
    return self.data.toxml()

class McbException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class Bixi:
  montrealStationsUrl = "https://profil.bixi.ca/data/bikeStations.xml"

def getXml(url):
  h = httplib2.Http(".cache")
  resp, content = h.request(url)
  if (resp.status != 200):
    raise McbException("Unexpected response status: expected '200' but got '" + str(resp.status) + "'")
  # FIXME this fails if no content-type specified
  if (resp['content-type'] != 'application/xml'):
    raise McbException("Unexpected response content-type: expected 'text/xml' but got '" + resp['content-type'] + "'")
  return content

def getBixiStationsXml():
  """Returns the XML representing the list of stations in Montreal"""
  return getXml(Bixi.montrealStationsUrl)

def convertBixiXml(xml, providerId):
  """Convert the Bixi XML format to the mycitybikes push format"""
  stations = ET.XML(xml)
  result = []
  for station in stations:
    station = xmlnode2dict(station)
    oldstation = station
    _station = dict_from_keys(station, dict(name='name',
                                      description='name',
                                      latitude='lat',
                                      longitude='long',
                                      ))
    #CHECK latitude and longitude
    #latitude and longitude must be  -90 <= X <=90
    try:
      lat = float(_station['latitude'])
      if lat > 90 or lat < -90:
        lat = 0
    except:
      lat = 0
    
    try:
      lng = float(_station['longitude'])
      if lng > 90 or lng < -90:
        lng = 0
    except:
      lng = 0
    _station['latitude'] = lat
    _station['longitude'] = lng
    ###############################
    
    stationStatus = dict_from_keys(station, dict(online='nbBikes',
                                             availableBikes='nbBikes',
                                             freeSlots='nbBikes',
                                             totalSlots='nbBikes'))
    _station['stationStatus'] = stationStatus
    result.append(_station)
    
  stations = result
  stations = [StationAndStatus(dict_to_xml(station, "stationAndStatus")) for station in stations]
  #doc = Document()
  #root_node = doc.createElement(unicode("stationAndstatuses",'utf-8'))
  #for station in stations:
  #    root_node.appendChild(station)
  #doc.appendChild(root_node)
  #xml = doc.toxml()
  #xml = xml.encode("utf-8")
  return stations

def getStationsAndStatuses(providerId):
  xml = getBixiStationsXml()
  return convertBixiXml(xml, providerId)

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

if __name__ == "__main__":
  PROVIDER_ID=MyCityBikes.getProviderForCity("Montreal").id
  updateStationAndStatuses(PROVIDER_ID)
