#!/usr/bin/python
# mycitybikes_montreal_bixi.py

from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO

MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")

# comment this out to test communication to the stubs
#MyCityBikes.enableMocks()

print "Starting Montreal,Bixi synchronization"

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
  if (resp['content-type'] != 'text/xml'):
    raise McbException("Unexpected response content-type: expected 'text/xml' but got '" + resp['content-type'] + "'")
  return content

def getBixiStationsXml():
  """Returns the XML representing the list of stations in Montreal"""
  return getXml(Bixi.montrealStationsUrl)

def convertBixiXml(xml, providerId):
  """Convert the Bixi XML format to the mycitybikes push format"""
  # FIXME implement
  return None

def getStationsAndStatuses(providerId):
  xml = getBixiStationsXml()
  return convertBixiXml(xml, providerId)

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

if __name__ == "__main__":
  PROVIDER_ID=MyCityBikes.getProviderForCity("Montreal").id
  updateStationAndStatuses(PROVIDER_ID)
