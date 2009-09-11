#! /usr/bin/python2.5
# -*- coding: utf-8 -*- 
from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulStoneSoup
from xml.dom.minidom import Document
from mycitybikes.mycitybikes import *
from utils import *
from encoding import force_unicode
MyCityBikes.setServerRoot("http://localhost:9000")
BARCELONA_URL = "http://www.bicing.com/general/estructura/base.php?TU5fTE9DQUxJWkFDSU9ORVM%3D&ZXM%3D&bG9jYWxpemFjaW9uZXMvbG9jYWxpemFjaW9uZXNfYm9keQ%3D%3D&MQ%3D%3D&&"

print "Starting Barcelona,Bicing synchronization"

class StationAndStatus:
  def __init__(self, data):
    self.__dict__ = data
    self.data = dict(data)
  def to_xml(self):
    element = dict_to_xml(self.data, "stationAndStatus")
    return element.toxml()
  
def getXml(url):
  h = httplib2.Http(".cache")
  resp, content = h.request(url)
  if (resp.status != 200):
    raise McbException("Unexpected response status: expected '200' but got '" + str(resp.status) + "'")
  # FIXME this fails if no content-type specified
  return content

def parse_node(node):
    try:
        description = node[0].text
        soup = BeautifulStoneSoup(description)
        divs = soup.findAll('div')
        name = divs[1].string.split('- ',1)[1]
        if name.endswith('/div>'):
          name = name[:-5]
        elif name.endswith('>'):
          name = name[:-1]
          
        bikes = divs[3].contents[0]
        aparcamientos = divs[3].contents[2] # TODO: find a translation and check the order    
        
        point = node[2][0].text.split(',')[:2]
        latitude, longitude = point
        latitude = tofloat(latitude)
        longitude = tofloat(longitude)
        if  not(-90 <= latitude <= 90):
          print latitude
          latitude = 0
        if not(-90 <= longitude <= 90):
          print longitude
          longitude = 0
          
    except Exception, e:
        print e
        return None
    
    station = dict(name=name,
                   description=name,
                   latitude=latitude,
                   longitude=longitude)
    #TODO: what should i do with these vars?
    station_status = dict(online=bikes,
                          availableBikes=bikes,
                          freeSlots=bikes,
                          totalSlots=bikes)
    station['stationStatus'] = station_status
    return station
                   

def getBarcelonaStationsXml():
  content = getXml(BARCELONA_URL)
  content = content.decode("utf-8","ignore").encode("utf-8","ignore")
  a = content.rindex("""<?xml""")
  b = content.rindex("""</kml>""")+6
  content = content[a:b]
  content = content.encode("utf-8")
  return content

def convertBarcelonaXml(xml, providerId):
  xml = ET.XML(xml)
  xml = xml.getchildren()[0]
  nodes = [node for node in xml if len(node.getchildren()) == 3]
  result = []
  for node in nodes:
    node = parse_node(node)
    if node:
      result.append(StationAndStatus(node))
  return result
  
def getStationsAndStatuses(providerId):
  xml = getBarcelonaStationsXml()
  return convertBarcelonaXml(xml, providerId)

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

        
if __name__ == "__main__":
  PROVIDER_ID=MyCityBikes.getProviderForCity("Barcelona").id
  updateStationAndStatuses(PROVIDER_ID)