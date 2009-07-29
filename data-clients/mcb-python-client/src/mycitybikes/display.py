#
# Simple helper methods to display data
#

def showCity(city):
  print "City id:%s\t%s,%s:\t(%s,%s)\t?? station(s)" % (city.id, city.name, city.country, city.latitude, city.longitude)

def showCities(cities):
  print "Found %s citie(s)" % (len(cities))
  for city in cities:
    showCity(city)

def showStation(station):
  print "Station id:%s\t%s\t%s\t(%s,%s)" % (station.id, station.cityId, station.description, station.latitude, station.longitude)

def showStations(stations):
  print "Found %s station(s)" % (len(stations))
  for station in stations:
    showStation(station)

def showStationStatus(stationStatus):
  print "Station cityId:%s,stationId:%s\t(bikes: %s, free:%s, total:%s)\t(%s)" % (stationStatus.cityId, stationStatus.stationId, stationStatus.availableBikes, stationStatus.freeSlots, stationStatus.totalSlots, stationStatus.updateDateTime)

def showStationStatuses(stationsStatuses):
  print "Found %s stationsStatuse(s)" % (len(stationsStatuses))
  for stationsStatus in stationsStatuses:
    showStationStatus(stationsStatus)

