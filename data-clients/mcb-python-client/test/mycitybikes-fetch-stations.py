#!/usr/bin/python
# mycitybikes-fetch-stations.py

from mycitybikes.mycitybikes import *

def showCity(city):
  print "City id:%s\t%s,%s:\t(%s,%s)\t?? station(s)" % (city.id, city.name, city.country, city.latitude, city.longitude)

def showCities(cities):
  print "Found %s citie(s)" % (len(cities))
  for city in cities:
    showCity(city)

# mycitybikes.MyCityBikes.setServerRoot("http://localhost/v1/")

MyCityBikes.enableMocks()

MyCityBikes.setServerRoot()
cities = MyCityBikes.getCities()
showCities(cities)

osloId = 1
oslo = MyCityBikes.getCity(osloId)

showCity(oslo)


