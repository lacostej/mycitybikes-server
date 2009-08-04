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
      if (subNode.tag == "providerId"):
        providerId = subNode.text
      if (subNode.tag == "externalId"):
        externalId = subNode.text
      if (subNode.tag == "name"):
        name = subNode.text
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
    return Station(stationId, providerId, externalId, name, description, latitude, longitude, creationDateTime, updateDateTime)

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
    print xml
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

  def putStationAndStatuses(providerId, stationAndStatuses):
    stationAndStatusesXml = []
    stationAndStatusesXml.append("</stationAndstatuses>")
    for stationAndStatus in stationAndStatuses:
      stationAndStatusesXml.append(stationAndStatus.to_xml())
    stationAndStatusesXml.append("</stationAndstatuses>")
    putContent = "".join(stationAndStatusesXml)
    LL.putStationAndStatuses(MyCityBikes.serverRoot, providerId, putContent)

  getCities = Callable(getCities)
  getCity = Callable(getCity)
  getStations = Callable(getStations)
  setStations = Callable(setStations)
  getStation = Callable(getStation)
  getStationStatuses = Callable(getStationStatuses)
  getStationStatus = Callable(getStationStatus)

  putStationAndStatuses = Callable(putStationAndStatuses)


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
  def __init__(self, id, providerId, externalId, name, description, latitude, longitude, creationDateTime=None, updateDateTime=None):
    self.id = id
    self.providerId = providerId
    self.externalId = externalId
    self.name = name
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.creationDateTime = creationDateTime
    self.updateDateTime = updateDateTime

  def to_xml(self):
    output = []
    output.append("<station>")
    # FIXME this won't be necessary once we make the reconciliation happen on the client
    if (self.id != None):
      output.append("<id>")
      output.append(self.id)
      output.append("</id>")
    output.append("<providerId>")
    output.append(self.providerId)
    output.append("</providerId>")
    output.append("<externalId>")
    output.append(self.externalId)
    output.append("</externalId>")
    if (self.name == None):
      output.append("<name/>")
    else:
      output.append("<name>")
      output.append(self.name)
      output.append("</name>")
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
  def __init__(self, providerId, stationId, online, availableBikes, freeSlots, totalSlots, updateDateTime=None):
    self.providerId = providerId
    self.stationId = stationId
    self.availableBikes = availableBikes
    self.freeSlots = freeSlots
    self.totalSlots = totalSlots
    self.online = online
    self.updateDateTime = updateDateTime

  def isOnline():
    return online == "1"

  def to_xml(self):
    output = []
    output.append("<stationStatus>")
    if (not self.providerId == None):
      output.append("<providerId>")
      output.append(self.providerId)
      output.append("</providerId>")
    if (not self.stationId == None):
      output.append("<stationId>")
      output.append(self.stationId)
      output.append("</stationId>")
    if (not self.online == None):
      output.append("<online>")
      output.append(self.online)
      output.append("</online>")
    if (not self.availableBikes == None):
      output.append("<availableBikes>")
      output.append(self.availableBikes)
      output.append("</availableBikes>")
    if (not self.freeSlots == None):
      output.append("<freeSlots>")
      output.append(self.freeSlots)
      output.append("</freeSlots>")
    if (not self.totalSlots == None):
      output.append("<totalSlots>")
      output.append(self.totalSlots)
      output.append("</totalSlots>")
    if (self.updateDateTime != None):
      output.append("<updateDateTime>")
      output.append(self.updateDateTime)
      output.append("</updateDateTime>")
    output.append("</stationAndStatus>")
    return ''.join(output)

class StationAndStatus:
  def __init__(self, providerId, externalId, name, description, latitude, longitude, stationStatus, updateDateTime):
    self.providerId = providerId
    self.externalId = externalId
    self.name = name
    self.description = description
    self.latitude = latitude
    self.longitude = longitude
    self.updateDateTime = updateDateTime
    self.stationStatus = stationStatus

  def to_xml(self):
    output = []
    output.append("<stationAndStatus>")
    output.append("<providerId>")
    output.append(self.providerId)
    output.append("</providerId>")
    output.append("<externalId>")
    output.append(self.externalId)
    output.append("</externalId>")
    if (self.name == None):
      output.append("<name/>")
    else:
      output.append("<name>")
      output.append(self.name)
      output.append("</name>")
    output.append("<description>")
    output.append(self.description.encode("utf-8"))
    output.append("</description>")
    output.append("<latitude>")
    output.append(self.latitude)
    output.append("</latitude>")
    output.append("<longitude>")
    output.append(self.longitude)
    output.append("</longitude>")
    output.append(self.stationStatus.to_xml())
    output.append("<updateDateTime>")
    output.append(self.updateDateTime.isoformat()+ "Z")
    output.append("</updateDateTime>")
    output.append("</stationAndStatus>")
    return ''.join(output)
