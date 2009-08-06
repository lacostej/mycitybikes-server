#!/usr/bin/python
# mycitybikes-oslo-clearchannel.py

from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO

#OSLO_PROVIDER_ID="5"
OSLO_PROVIDER_ID="4"

#MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")
MyCityBikes.setServerRoot("http://localhost")

# comment this out to test communication to the stubs
#MyCityBikes.enableMocks()

print "Starting Oslo,ClearChannel synchronization"

class McbException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def getClearChannelXml(url):
  h = httplib2.Http(".cache")
  resp, content = h.request(url)
  if (resp.status != 200):
    raise McbException("Unexpected response status: expected '200' but got '" + str(resp.status) + "'")
  # FIXME this fails if no content-type specified
  if (resp['content-type'] == 'text/xml'):
    raise McbException("Unexpected response content-type: expected 'text/xml' but got '" + resp['content-type'] + "'")
  return content

def getStationsXml():
  """Returns the XML representing the list of stations in Oslo"""
  return getClearChannelXml("http://smartbikeportal.clearchannel.no/public/mobapp/maq.asmx/getRacks")

def getStationInfoXml(id):
  """Returns the XML representing the station information (and status) for a particular station id in Oslo."""
  return getClearChannelXml("http://smartbikeportal.clearchannel.no/public/mobapp/maq.asmx/getRack?id=" + id)


def getStationIds(xml):
  """Return a list of ids (strings) representing """
  stringNode = ET.XML(xml)
  if not stringNode.tag == "{http://smartbikeportal.clearchannel.no/public/mobapp/}string":
    raise McbException("Incorrect format: expected 'string' unexpected root tree '" + stringNode.tag + "'")

  stationsXml = "<stations>" + stringNode.text + "</stations>"
  stationsNode = ET.XML(stationsXml)

  ids = []
  for stationNode in stationsNode:
    if not stationNode.tag == "station":
      raise McbException("Incorrect format: expected 'station' sub node but got '" + stationNode.tag + "'")
    ids.append(stationNode.text)
  return ids

class OsloStation:
  def __init__(self, externalId, description, latitude, longitude, status):
    self.externalId = externalId
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.status = status

  def __str__(self):
    if self.status == None:
      statusStr = "No Status"
    else:
      statusStr = str(self.status)
    l = [self.externalId, self.description, self.latitude, self.longitude, statusStr]
    return "-".join(l)

class OsloStationStatus:
  def __init__(self, readyBikes, emptyLocks, online):
    self.readyBikes = readyBikes
    self.emptyLocks = emptyLocks
    self.online = online

  def totalLocks(self):
    """Return the totalSlots as a String"""
    if (self.readyBikes == None):
      return None
    return unicode(int(self.readyBikes) + int(self.emptyLocks))

  def __str__(self):
    l = [self.readyBikes, self.emptyLocks, self.online]
    return "Status(" + "-".join(l) + ")"


def getStation(externalId, xml):
  """Return the station object for Oslo"""
  stringNode = ET.XML(xml)
  if not stringNode.tag == "{http://smartbikeportal.clearchannel.no/public/mobapp/}string":
    raise McbException("Incorrect format: expected 'string' unexpected root tree '" + stringNode.tag + "'")

  text = stringNode.text.replace("&", "&amp;").encode("utf-8")
  stationNode = ET.XML(text)

  if not stationNode.tag == "station":
    raise McbException("Unexpected root node in station: '" + stationNode.tag + "'")

  readyBikes = None
  for subNode in stationNode:
    if subNode.tag == "description":
      description = subNode.text.strip().replace("&", "&amp;").encode("utf-8")
      array = description.partition("-")
      if not len(array[1]) == 0:
        description = array[2]
    elif subNode.tag == "longitute": # Sic...
      longitude = subNode.text
    elif subNode.tag == "latitude":
      latitude = subNode.text
    elif subNode.tag == "ready_bikes":
      readyBikes = subNode.text
    elif subNode.tag == "empty_locks":
      emptyLocks = subNode.text
    elif subNode.tag == "online":
      online = subNode.text
    else:
      raise McbException("Unexpected node in station: '" + subNode.tag + "'")
  if (readyBikes == None):
    status = OsloStationStatus(None, None, "0")
  else:
    status = OsloStationStatus(readyBikes, emptyLocks, online)
  return OsloStation(externalId, description, latitude, longitude, status)

xml = getStationsXml()
ids = getStationIds(xml)

#x = getStationInfoXml("1");
#print x
#print getStation("1", x)

# to test &amp; handling
#x = getStationInfoXml("66");
#print x
#print getStation("66", x)

def getStationsAndStatuses(providerId):
  stationAndStatuses = []
  for id in ids:
    # filter out invalid/test stations
    if (int(id) >= 500): 
      print "Skipping station " + id
      continue

    stationXml = getStationInfoXml(id);
    station = getStation(id, stationXml)

    stationStatus = StationStatus(None, None, station.status.online, station.status.readyBikes, station.status.emptyLocks, station.status.totalLocks(), None)
    stationAndStatus = StationAndStatus(providerId, station.externalId, None, station.description, station.latitude, station.longitude, stationStatus, datetime.utcnow())
    stationAndStatuses.append(stationAndStatus)
  return stationAndStatuses

def updateStationAndStatuses(providerId):
  stationAndStatuses = getStationsAndStatuses(providerId)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

#def __usage():
#  print "USAGE: " + sys.argv[0] + " providerId assetfilepath"
#  print "\tproviderId\tthe id of the provider that manages the stations"
#  print "\tassetfilepath\tthe path of the file containing the android client XML assets"

if __name__ == "__main__":
#  import sys
#  if (len(sys.argv) < 2):
#    print "ERROR: Missing providerId argument"
#    __usage()
#    exit()
#  if (len(sys.argv) < 3):
#    print "ERROR: Missing input filepath argument"
#    __usage()
#    exit()

#  providerId = sys.argv[1]
#  inputfile = sys.argv[2]

  updateStationAndStatuses(OSLO_PROVIDER_ID)



  # algo estimates
  # 1 put for station and one for stationstatus every minute no matter what. ~100 stations, runs every minute i.e. 1500 time per day, 2 queries, would be 300 000 queries
  # 1 put for all station and statuses at once ~100 stations, runs every minute, i.e. 1500 times per day

  # FIXME add update timestamp
  # 1. convert Station and its Status to mycibikes.BikeStation and StationStatus objects
  # 2. put station and status online
  # on server
  # search station by providerId and externalId
  #   if Station doesn't exist, create it
  #   if Station exists, check the difference update it if necessary
  # 3. IMPROVEMENT clean up old stations
