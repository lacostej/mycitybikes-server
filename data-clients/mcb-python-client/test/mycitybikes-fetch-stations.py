#!/usr/bin/python
# mycitybikes-fetch-stations.py

from mycitybikes.mycitybikes import *

# comment this out to test communication to the stubs
#MyCityBikes.enableMocks()

# change the server you're talking to
#MyCityBikes.setServerRoot("http://localhost/v1/")
#MyCityBikes.setServerRoot("http://190.186.22.131")
MyCityBikes.setServerRoot("http://localhost")
# used to reset the server root
#MyCityBikes.setServerRoot()


#
# 
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


# MyCityBikes.getStations(1, [1,2])

cities = MyCityBikes.getCities()
showCities(cities)

osloId = "1"
oslo = MyCityBikes.getCity(osloId)

showCity(oslo)

stations = MyCityBikes.getStations(1)

showStations(stations)

stationStatuses = MyCityBikes.getStationStatuses(1)

showStationStatuses(stationStatuses)
