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

class Washington:
  Url = "https://www.smartbikedc.com/smartbike_locations.asp"
  
class StationAndStatus:
  def __init__(self, data):
    self.__dict__ = data
    self.data = dict(data)
  def to_xml(self):
    element = dict_to_xml(self.data, "stationAndStatus")
    return element.toxml()

def getHTML(url):
  h = httplib2.Http(".cache")
  resp, content = h.request(url)
  if (resp.status != 200):
    raise McbException("Unexpected response status: expected '200' but got '" + str(resp.status) + "'")
  # FIXME this fails if no content-type specified
  #if (resp['content-type'] not in  ['application/xml', 'text/xml']):
  #  raise McbException("Unexpected response content-type: expected 'text/xml' but got '" + resp['content-type'] + "'")
  return content

def getWashingtonStationsHTML():
  return getHTML(Washington.Url)

def convertWashingtonHTML(html, providerId):
  a,b=html.index("""//<![CDATA["""), html.index("""//]]>""")
  html = html[a:b]
  lines = iter(html.splitlines())
  stations = [] 
  for line in lines:
      if STATION_RE.match(line):
          start=line.index('.')+1
          line = line[start:].strip()
          line = line[:line.index(',')]
          line = line[:line.rindex(' ')]
          name = line
          lines.next()
          point = lines.next()
          latitude, longitude = POINT_RE.match(point).groups()
          
          lines.next()
          address = lines.next().split('=')[1]
          address = address.replace("<br />", " ")[1:-2]
          lines.next()
          lines.next()
          lines.next()
          station_info = lines.next()
          info = STATIONINFO_RE.match(station_info).groups()
          readyBikes, emptyLocks = info
          station = dict(name=name,
                         description=address,
                         latitude=latitude,
                         longitude=longitude)
    
          station_status = dict(online=readyBikes, # check this
                                availableBikes=readyBikes,
                                freeSlots=emptyLocks,
                                totalSlots=0) #checkthis
          station['stationStatus'] = station_status
          stations.append(station)
  result = []
  for station in stations:
    result.append(StationAndStatus(station))
  return result


def getStationsAndStatuses(providerId):
  html = getWashingtonStationsHTML()
  return convertWashingtonHTML(html, providerId)
  

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

if __name__ == "__main__":
  PROVIDER_ID=MyCityBikes.getProviderForCity("Washington").id
  updateStationAndStatuses(PROVIDER_ID)
        
        
        
