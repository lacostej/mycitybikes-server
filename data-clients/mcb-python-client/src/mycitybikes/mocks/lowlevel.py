import httplib2

PROLOGUE='<?xml version="1.0" encoding="utf-8" ?>'

OSLO="<city><id>1</id><name>Oslo</name><country>Norway</country><latitude>59.913821</latitude><longitude>10.738739</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></city>"
PARIS="<city><id>2</id><name>Paris</name><country>France</country><latitude>48.856666</latitude><longitude>2.350986</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></city>"
STOCKHOLM="<city><id>3</id><name>Stockholm</name><country>Sweeden</country><latitude>61.143235</latitude><longitude>9.09668</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></city>"

OSLO_STATION_1=ur'<station><id>1</id><providerId>1</providerId><externalId>01</externalId><name>01</name><description>Vestbanen S\u00f8r (v/Aker Brygge)</description><latitude>59.9109</latitude><longitude>10.72935</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></station>'

OSLO_STATION_2=ur'<station><id>1</id><providerId>1</providerId><externalId>02</externalId><name>02</name><description>Ullev\u00e5lsveien 9 v/V\u00e5r Frues hospital,ovenf Barnevognhuset</description><latitude>59.91953799289473</latitude><longitude>10.743963718414306</longitude><creationDateTime>2009-07-28T16:47:00.000Z</creationDateTime><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></station>'

OSLO_STATION_STATUS_1=ur'<stationStatus><cityId>1</cityId><stationId>1</stationId><availableBikes>8</availableBikes><freeSlots>3</freeSlots><totalSlots>11</totalSlots><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></stationStatus>'

OSLO_STATION_STATUS_2=ur'<stationStatus><cityId>1</cityId><stationId>2</stationId><availableBikes>3</availableBikes><freeSlots>0</freeSlots><totalSlots>4</totalSlots><updateDateTime>2009-07-28T16:48:00.000Z</updateDateTime></stationStatus>'

PROVIDERS=ur'<providers><provider><id>7</id><cityId>2</cityId><updateDateTime>2009-07-30T14:41:20.292416Z</updateDateTime><locationsUpdated>2009-07-30T10:41:15Z</locationsUpdated><shortName>ClearChannel</shortName><creationDateTime>2009-07-30T14:41:20.292416Z</creationDateTime><fullName>ClearChannel,Oslo</fullName></provider><provider><id>9</id><cityId>3</cityId><updateDateTime>2009-07-30T14:41:40.065964Z</updateDateTime><locationsUpdated>2009-07-30T10:41:36Z</locationsUpdated><shortName>ClearChannel</shortName><creationDateTime>2009-07-30T14:41:40.065964Z</creationDateTime><fullName>ClearChannel,Stocholm</fullName></provider><provider><id>11</id><cityId>1</cityId><updateDateTime>2009-07-30T14:41:56.772936Z</updateDateTime><locationsUpdated>2009-07-30T10:41:53Z</locationsUpdated><shortName>JCDecaux</shortName><creationDateTime>2009-07-30T14:41:56.772936Z</creationDateTime><fullName>JCDecaux,Paris</fullName></provider></providers>'

def __u(s):
  return s.encode("utf-8")

def info():
  return "lowlevel MOCKS mycitybikes lib"

def getCities(serverRoot, cityIds=None):
  return __u((PROLOGUE+"<cities>" + OSLO + PARIS + STOCKHOLM + "</cities>"))

def getProviders(serverRoot):
  return __u((PROLOGUE+PROVIDERS))

def getCity(serverRoot, cityId):
  return __u(PROLOGUE+OSLO)

def getStations(serverRoot, cityId, stationIds=None):
  return __u(PROLOGUE+"<stations>" + OSLO_STATION_1 + OSLO_STATION_2 + "</stations>")

def getStation(serverRoot, cityId, stationId):
  return __u(PROLOGUE+OSLO_STATION_1)

def getStationStatuses(serverRoot, cityId, stationIds=None):
  return __u(PROLOGUE+"<stationStatuses>" + OSLO_STATION_STATUS_1 + OSLO_STATION_STATUS_2 + "</stationStatuses>" )

def getStationStatus(serverRoot, cityId, stationId):
  return __u(PROLOGUE+OSLO_STATION_STATUS_1 )

def putStationAndStatuses(serverRoot, providerId, putContent):
  print serverRoot + " putStationAndStatuses(" + providerId + ")"
  print putContent
