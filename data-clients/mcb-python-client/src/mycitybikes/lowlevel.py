import httplib2


def info():
  return "lowlevel mycitybikes lib"

# @param serverRoot the url of the serverRoot
# @param cityIds the list of ids of the cities to retrieve. None to retrieve them all
def getCities(serverRoot, cityIds=None):
  h = httplib2.Http(".cache")
  resp, content = h.request(serverRoot + "/cities.xml")
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city to retrieve
def getCity(serverRoot, cityId):
  h = httplib2.Http(".cache")
  resp, content = h.request(serverRoot + "/cities/" + cityId + ".xml")
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationsIds the list of ids of the stations to retrieve. None to retrieve them all
def getCityStations(serverRoot, cityId, stationIds=None):
  return "<stations/>"

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationsIds the list of ids of the stations to retrieve. None to retrieve them all
def getStationsStatuses(serverRoot, cityId, stationIds=None):
  return "<stationStatuses/>"



