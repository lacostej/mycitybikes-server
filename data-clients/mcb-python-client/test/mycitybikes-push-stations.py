#!/usr/bin/python
# mycitybikes-push-stations.py

#
# update a city's stations
# 
# $0 cityName file.xml
#

from mycitybikes.mycitybikes import *
from mycitybikes.utils import *
from mycitybikes.display import *

from convert_android_assets import *

# comment this out to test communication to the stubs
# MyCityBikes.enableMocks()

# change the server you're talking to
#MyCityBikes.setServerRoot("http://localhost:8000")
#MyCityBikes.setServerRoot("http://190.186.22.131")

# used to reset the server root
#MyCityBikes.setServerRoot()
MyCityBikes.setServerRoot("http://localhost")

cities = MyCityBikes.getCities()
stockholm = cities[index(cities, lambda city: city.name == 'Stockholm')]

# FIXME when we introduce Providers
stockholmProviderId = stockholm.id
#providers = MyCityBikes.getProviders()
#stockholmProvider = providers[index(providers, lambda provider: provider.cityId == stockholm.id)]
#showProvider(stockholmProvider)
#stockholmProviderId = stockholmProvider.id

stations = getStationsFromAndroidAssetFile('assets/stockholm.xml', stockholmProviderId)

MyCityBikes.setStations(stockholmProviderId, stations)

newStations = MyCityBikes.getStations(stockholm.id)
showStations(newStations)
