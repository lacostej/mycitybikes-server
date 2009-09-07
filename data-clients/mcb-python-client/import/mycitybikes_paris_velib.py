import re
STATION_RE = re.compile("""// \d""")
STATIONINFO_RE = re.compile(""".*<font color=red>([0-9]*)</font>.*Slots: ([0-9]*)<br>.*""")
POINT_RE = re.compile(""".*\\((.*),(.*)\\).*""")
#!/usr/bin/python
# mycitybikes_montreal_bixi.py

from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO
from xml.dom.minidom import Document
from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB
from utils import *
#MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")
MyCityBikes.setServerRoot("http://localhost:9000")

class McbException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
  
class Paris:
  Url = "http://www.velib.paris.fr/service/carto"
  UrlStation = "http://www.velib.paris.fr/service/stationdetails/%s"
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
  print "URL ====> %s" % url
  if (resp.status != 200):
    raise McbException("Unexpected response status: expected '200' but got '" + str(resp.status) + "'")
  # FIXME this fails if no content-type specified
  if (resp['content-type'] not in  ['application/xml', 'text/xml', 'text/xml; charset=utf-8']):
    raise McbException("Unexpected response content-type: expected 'text/xml' but got '" + resp['content-type'] + "'")
  return content

def getParisStationsXml():
  return getXml(Paris.Url)

def convertParisXml(xml, providerId):
  children = ET.XML(xml)[0].getchildren()
  stations = [] 
  for child in children:
    fields = child.attrib
    station = dict_from_keys(fields, dict(name='name',
                                          latitude='lat',
                                          longitude='lon',
                                          description='fullAddress',
                                          number='number'))
    station['name']  = station['name'].split('-')[1].strip()
    station['longitude'] = tofloat(station['longitude'])
    station['latitude'] = tofloat(station['latitude'])
    if not (-90 <= station['longitude'] <= 90):
      continue
    if not (-90 <= station['latitude'] <= 90):
      continue    
    url = Paris.UrlStation%fields['number']
    print "URL %s" % url
    stationstatus = ET.XML(getXml(url))
    station_status = dict(
                          availableBikes=stationstatus[0].text,
                          freeSlots=stationstatus[1].text,
                          totalSlots=stationstatus[2].text) #checkthis
    station['stationStatus'] = station_status
    stations.append(station)
  result = []
  for station in stations:
    result.append(StationAndStatus(station))
  return result


def getStationsAndStatuses(providerId):
  html = getParisStationsXml()
  return convertParisXml(html, providerId)
  

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

if __name__ == "__main__":
  PROVIDER_ID=MyCityBikes.getProviderForCity("Paris").id
  print "----> %s" % PROVIDER_ID
  updateStationAndStatuses(PROVIDER_ID)
        
        
        
