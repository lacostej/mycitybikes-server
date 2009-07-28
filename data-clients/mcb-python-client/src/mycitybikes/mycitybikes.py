import xml.etree.ElementTree as ET
import lowlevel as LL
from StringIO import StringIO

# pyXML (python-xml in debian/ubuntu)
from xml.utils.iso8601 import parse

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
        id = subNode.text
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
    return Station(id, cityId, description, latitude, longitude, creationDateTime, updateDateTime)

  __parseCityNode = Callable(__parseCityNode)
  __parseStationNode = Callable(__parseStationNode)

  def getCities():
    #print "using " + LL.info()
    xml = LL.getCities(MyCityBikes.serverRoot, None)
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
#    node = ET.parse(StringIO(xml))
    stations = []
    for stationNode in node:
      stations.append(MyCityBikes.__parseStationNode(stationNode))
    return stations

  def getStation(cityId, stationId):
    stationXml = LL.getStations(MyCityBikes.serverRoot, cityId, [stationId])
    stationNode = ET.XML(stationXml)
    return MyCityBikes.__parseStationNode(stationNode)

  getCities = Callable(getCities)
  getCity = Callable(getCity)
  getStations = Callable(getStations)
  getStation = Callable(getStation)

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
  def __init__(self, id, cityId, description, latitude, longitude, creationDateTime, updateDateTime):
    self.id = id
    self.cityId = cityId
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.creationDateTime = creationDateTime
    self.updateDateTime = updateDateTime

class StationStatus:
  pass
