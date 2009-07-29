import xml.etree.ElementTree as ET
import lowlevel as LL
from StringIO import StringIO

# pyXML (python-xml in debian/ubuntu)

try:
  from xml.utils.iso8601 import parse
except ImportError:
  print "Couldn't load iso8601 from system. Using one from library"
  from lib.iso8601 import parse

class Callable:
  def __init__(self, anycallable):
    self.__call__ = anycallable


# a class with static methods to fetch the data root (cities) and initialize some settings (server root url, mocks, ...)
class MyCityBikes:
  DEFAULT_SERVER_ROOT = "https://mycitybikes.appspot.com/v1/"
  serverRoot = DEFAULT_SERVER_ROOT

  # no argument resets to default
  def setServerRoot(sr=DEFAULT_SERVER_ROOT):
    MyCityBikes.serverRoot=sr

  def getServerRoot():
    return MyCityBikes.serverRoot

  # ugly way to override the import of the mock lowlevel library
  def enableMocks():
    import mocks.lowlevel as ll
    global LL
    LL = ll

  setServerRoot = Callable(setServerRoot)
  getServerRoot = Callable(getServerRoot)
  enableMocks = Callable(enableMocks)

  # @param an Element representing the City
  # @return a City object representing the specified cityNode
  def __parseCityNode(cityNode):
    for subNode in cityNode:
      if (subNode.tag == "id"):
        id = subNode.text
      if (subNode.tag == "name"):
        name = subNode.text
      if (subNode.tag == "country"):
        country = subNode.text
      if (subNode.tag == "latitude"):
        latitude = subNode.text
      if (subNode.tag == "longitude"):
        longitude = subNode.text
      if (subNode.tag == "creationDateTime"):
        creationDateTime = parse(subNode.text)
      if (subNode.tag == "updateDateTime"):
        updateDateTime = parse(subNode.text)
    return City(id, name, country, latitude, longitude, creationDateTime, updateDateTime)

  # @param an Element representing the Station
  # @return a Station object representing the specified stationNode
  def __parseStationNode(stationNode):
    for subNode in stationNode:
      if (subNode.tag == "id"):
        stationId = subNode.text
      if (subNode.tag == "cityId"):
        cityId = subNode.text
      if (subNode.tag == "description"):
        description = subNode.text
      if (subNode.tag == "latitude"):
        latitude = subNode.text
      if (subNode.tag == "longitude"):
        longitude = subNode.text
      if (subNode.tag == "creationDateTime"):
        creationDateTime = parse(subNode.text)
      if (subNode.tag == "updateDateTime"):
        updateDateTime = parse(subNode.text)
    return Station(stationId, cityId, description, latitude, longitude, creationDateTime, updateDateTime)

  # @param an Element representing the StationStatus
  # @return a StationStatus object representing the specified stationStatusNode
  def __parseStationStatusNode(stationStatusNode):
    for subNode in stationStatusNode:
      if (subNode.tag == "cityId"):
        cityId = subNode.text
      if (subNode.tag == "stationId"):
        stationId = subNode.text
      if (subNode.tag == "availableBikes"):
        availableBikes = subNode.text
      if (subNode.tag == "freeSlots"):
        freeSlots = subNode.text
      if (subNode.tag == "totalSlots"):
        totalSlots = subNode.text
#      if (subNode.tag == "creationDateTime"):
#        creationDateTime = parse(subNode.text)
      if (subNode.tag == "updateDateTime"):
        updateDateTime = parse(subNode.text)
    return StationStatus(cityId, stationId, availableBikes, freeSlots, totalSlots, updateDateTime)

  __parseCityNode = Callable(__parseCityNode)
  __parseStationNode = Callable(__parseStationNode)
  __parseStationStatusNode = Callable(__parseStationStatusNode)

  def getCities():
    #print "using " + LL.info()
    xml = LL.getCities(MyCityBikes.serverRoot, None)
    #print xml
    node = ET.XML(xml)
    cities = []
    for cityNode in node:
      cities.append(MyCityBikes.__parseCityNode(cityNode))
    return cities

  def getCity(cityId):
    xml = LL.getCity(MyCityBikes.serverRoot, cityId)
    node = ET.XML(xml)
    return MyCityBikes.__parseCityNode(node)

  def getStations(cityId, stationIds=None):
    xml = LL.getStations(MyCityBikes.serverRoot, cityId, stationIds)
    node = ET.XML(xml)
    stations = []
    for stationNode in node:
      stations.append(MyCityBikes.__parseStationNode(stationNode))
    return stations

  def setStations(providerId, stations):
    xml = StationList.to_xml(stations)
    LL.setStations(MyCityBikes.serverRoot, providerId, xml)

  def getStation(cityId, stationId):
    xml = LL.getStation(MyCityBikes.serverRoot, cityId, stationId)
    node = ET.XML(xml)
    return MyCityBikes.__parseStationNode(node)

  def getStationStatuses(cityId, stationIds=None):
    xml = LL.getStationStatuses(MyCityBikes.serverRoot, cityId, stationIds)
    node = ET.XML(xml)
    stationStatuses = []
    for stationStatusNode in node:
      stationStatuses.append(MyCityBikes.__parseStationStatusNode(stationStatusNode))
    return stationStatuses

  def getStationStatus(cityId, stationId):
    xml = LL.getStationStatus(MyCityBikes.serverRoot, cityId, stationId)
    node = ET.XML(xml)
    return MyCityBikes.__parseStationStatusNode(node)

  getCities = Callable(getCities)
  getCity = Callable(getCity)
  getStations = Callable(getStations)
  setStations = Callable(setStations)
  getStation = Callable(getStation)
  getStationStatuses = Callable(getStationStatuses)
  getStationStatus = Callable(getStationStatus)


class City:
  def __init__(self, id, name, country, latitude, longitude, creationDateTime, updateDateTime):
    self.id = id
    self.name = name
    self.country = country
    self.latitude = latitude
    self.longitude = longitude
    self.creationDateTime = creationDateTime
    self.updateDateTime = updateDateTime

class Station:
  def __init__(self, id, cityId, description, latitude, longitude, creationDateTime=None, updateDateTime=None):
    self.id = id
    self.cityId = cityId
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.creationDateTime = creationDateTime
    self.updateDateTime = updateDateTime

  def to_xml(self):
    output = []
    output.append("<station>")
    output.append("<id>")
    output.append(self.id)
    output.append("</id>")
    output.append("<cityId>")
    output.append(self.cityId)
    output.append("</cityId>")
    output.append("<description>")
    output.append(self.description.encode("utf-8"))
    output.append("</description>")
    output.append("<latitude>")
    output.append(self.latitude)
    output.append("</latitude>")
    output.append("<longitude>")
    output.append(self.longitude)
    output.append("</longitude>")
    if (self.creationDateTime != None):
      output.append("<creationDateTime>")
      output.append(self.creationDateTime)
      output.append("</creationDateTime>")
    if (self.updateDateTime != None):
      output.append("<updateDateTime>")
      output.append(self.updateDateTime)
      output.append("</updateDateTime>")
    output.append("</station>")
    return ''.join(output)

class StationList:
  # @param a list of Station instances
  def to_xml(stations):
    """Helper method to convert a list of Station into xml"""
    l = []
    l.append("<stations>")
    for station in stations:
      l.append(station.to_xml())
    l.append("</stations>")
    return ''.join(l)

  to_xml = Callable(to_xml)

class StationStatus:
  def __init__(self, cityId, stationId, availableBikes, freeSlots, totalSlots, updateDateTime):
    self.cityId = cityId
    self.stationId = stationId
    self.availableBikes = availableBikes
    self.freeSlots = freeSlots
    self.totalSlots = totalSlots
    self.updateDateTime = updateDateTime
