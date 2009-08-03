#!/usr/bin/python
# mycitybikes-fetch-stations.py

from mycitybikes.mycitybikes import *
from mycitybikes.display import *
from mycitybikes.utils import *

# comment this out to test communication to the stubs
# MyCityBikes.enableMocks()

# change the server you're talking to
MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")
#MyCityBikes.setServerRoot("http://localhost:8000")
#MyCityBikes.setServerRoot("http://190.186.22.131")
#MyCityBikes.setServerRoot("http://localhost")
# used to reset the server root
# MyCityBikes.setServerRoot()


# MyCityBikes.getStations(1, [1,2])

cities = MyCityBikes.getCities()
showCities(cities)


oslo = cities[index(cities, lambda city: city.name == 'Oslo')]

# fetch again to test getCity
oslo = MyCityBikes.getCity(oslo.id)
showCity(oslo)

stations = MyCityBikes.getStations(oslo.id)
showStations(stations)

stationId = stations[0].id

station = MyCityBikes.getStation(oslo.id, stationId)
showStation(station)


stationStatuses = MyCityBikes.getStationStatuses(oslo.id)
showStationStatuses(stationStatuses)

stationStatus = MyCityBikes.getStationStatus(oslo.id, stationId)
showStationStatus(stationStatus)
