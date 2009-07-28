import xml.etree.ElementTree as ET
import lowlevel as LL

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
    for citySubNode in cityNode:
      if (citySubNode.tag == "id"):
        id = citySubNode.text
      if (citySubNode.tag == "name"):
        name = citySubNode.text
      if (citySubNode.tag == "country"):
        country = citySubNode.text
      if (citySubNode.tag == "latitude"):
        latitude = citySubNode.text
      if (citySubNode.tag == "longitude"):
        longitude = citySubNode.text
      if (citySubNode.tag == "creationDateTime"):
        creationDateTime = parse(citySubNode.text)
      if (citySubNode.tag == "updateDateTime"):
        updateDateTime = parse(citySubNode.text)
    return City(id, name, country, latitude, longitude, creationDateTime, updateDateTime)

  __parseCityNode = Callable(__parseCityNode)

  def getCities():
    #print "using " + LL.info()
    citiesXml = LL.getCities(MyCityBikes.serverRoot, None)
    citiesNode = ET.XML(citiesXml)
    cities = []
    for cityNode in citiesNode:
      cities.append(MyCityBikes.__parseCityNode(cityNode))
    return cities

  def getCity(cityId):
    cityXml = LL.getCity(MyCityBikes.serverRoot, cityId)
    cityNode = ET.XML(cityXml)
    return MyCityBikes.__parseCityNode(cityNode)

  getCities = Callable(getCities)
  getCity = Callable(getCity)

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
  pass

class StationStatus:
  pass
