import httplib2

OSLO="<city><id>1</id><name>Oslo</name><country>Norway</country><latitude>59.913821</latitude><longitude>10.738739</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></city>"
PARIS="<city><id>2</id><name>Paris</name><country>France</country><latitude>48.856666</latitude><longitude>2.350986</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></city>"

def info():
  return "lowlevel MOCKS mycitybikes lib"

def getCities(serverRoot, cityIds=None):
  return "<cities>" + OSLO + PARIS + "</cities>"

def getCity(serverRoot, cityId):
  return OSLO

def getCityStations(serverRoot, cityId, stationIds=None):
  return "<stations/>"

def getStationsStatuses(serverRoot, cityId, stationIds=None):
  return "<stationStatuses/>"



