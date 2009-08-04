#!/usr/bin/python
# mycitybikes-oslo-clearchannel.py

from mycitybikes import *

import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO

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

class Station:
  def __init__(self, osloId, description, latitude, longitude, status):
    self.osloId = osloId
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.status = status

  def __str__(self):
    if self.status == None:
      statusStr = "No Status"
    else:
      statusStr = str(self.status)
    l = [self.osloId, self.description, self.latitude, self.longitude, statusStr]
    return "-".join(l)

class StationStatus:
  def __init__(self, readyBikes, emptyLocks, online):
    self.readyBikes = readyBikes
    self.emptyLocks = emptyLocks
    self.online = online

  def __str__(self):
    l = [self.readyBikes, self.emptyLocks, self.online]
    return "Status(" + "-".join(l) + ")"


def getStation(osloId, xml):
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
      description = subNode.text.strip().encode("utf-8")
#      print type(len(description))
#      print type(description.find("-"))
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
    status = None
  else:
    status = StationStatus(readyBikes, emptyLocks, online)
  return Station(osloId, description, latitude, longitude, status)

xml = getStationsXml()
ids = getStationIds(xml)

#x = getStationInfoXml("1");
#print x
#print getStation("1", x)

# to test &amp; handling
#x = getStationInfoXml("66");
#print x
#print getStation("66", x)

for id in ids:
  station = getStationInfoXml(id);
  # filter out unwanted stations
  if (int(id) >= 500): 
    print "Skipping station " + id
    continue
  print getStation(id, station)

