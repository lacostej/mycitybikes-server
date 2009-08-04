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
  # FIXME this fails if no content-type specified
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city to retrieve
def getCity(serverRoot, cityId):
  h = httplib2.Http(".cache")
  resp, content = h.request(serverRoot + "/cities/" + str(cityId) + ".xml")
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

#def updateCity(serverRoot, cityId, cityXml):
#  h = httplib2.Http(".cache")
#  resp, content = h.request(serverRoot + "/cities" + cityId + ".xml", "PUT", body=cityXml, headers = {'content-type': 'text/xml'})
#  if (resp.status != 200):
#    # FIXME
#    pass
#  if (resp['content-type'] == 'text/xml'):
#    # FIXME
#    pass

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationsIds the list of ids of the stations to retrieve. None to retrieve them all
def getStations(serverRoot, cityId, stationIds=None):
  h = httplib2.Http(".cache")
  if (stationIds == None):
    ids = "all"
  else:
#    ids = str.join(',', stationIds)
    ids = ','.join([`num` for num in stationIds])
  url = serverRoot + "/stations/city/" + str(cityId) + "/" + ids + ".xml"
  print url
  resp, content = h.request(url)
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param providerId the id of the provider that controls the stations
# @param stationsXml the xml representing the stations
def setStations(serverRoot, providerId, stationsXml):
  h = httplib2.Http(".cache")
  url = serverRoot + "/stations/provider/" + str(providerId) + "/all.xml"
  print url
  resp, content = h.request(url, "PUT", body=stationsXml, headers = {'content-type': 'text/xml'})
  if (resp.status != 200):
    print resp
    # FIXME
    pass
#  if (resp['content-type'] == 'text/xml'):
#    # FIXME
#    pass
#  return content


# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationId the id of the station to retrieve
def getStation(serverRoot, cityId, stationId):
  h = httplib2.Http(".cache")
  url = serverRoot + "/stations/city/" + str(cityId) + "/" + str(stationId) + ".xml"
  resp, content = h.request(url)
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
# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationsIds the list of ids of the stations to retrieve. None to retrieve them all
def getStationStatuses(serverRoot, cityId, stationIds=None):
  h = httplib2.Http(".cache")
  if (stationIds == None):
    ids = "all"
  else:
#    ids = str.join(',', stationIds)
    ids = ','.join([`num` for num in stationIds])
  url = serverRoot + "/stationStatuses/city/" + str(cityId) + "/" + ids + ".xml"
  print url
  resp, content = h.request(url)
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationId the id of the station to retrieve
def getStationStatus(serverRoot, cityId, stationId):
  h = httplib2.Http(".cache")
  url = serverRoot + "/stationStatuses/city/" + str(cityId) + "/" + str(stationId) + ".xml"
  resp, content = h.request(url)
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content

# @param serverRoot the url of the serverRoot
# @param cityId the id of the city that contains the stations
# @param stationId the id of the station to retrieve
def putStationAndStatuses(serverRoot, providerId, putContent):
  h = httplib2.Http(".cache")
  url = serverRoot + "/stationAndStatuses/provider/" + str(providerId) + "/all.xml"
  resp, content = h.request(url, "PUT", body=putContent, headers = {'content-type': 'text/xml'})
  if (resp.status != 200):
    # FIXME
    pass
  if (resp['content-type'] == 'text/xml'):
    # FIXME
    pass
  return content
