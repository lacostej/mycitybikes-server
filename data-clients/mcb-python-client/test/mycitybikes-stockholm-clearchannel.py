#!/usr/bin/python
# mycitybikes-stockholm-clearchannel.py

from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO

#MyCityBikes.setServerRoot("http://mycitybikes.appspot.com")
MyCityBikes.setServerRoot("http://localhost")

# comment this out to test communication to the stubs
#MyCityBikes.enableMocks()

print "Starting Oslo,ClearChannel synchronization"

class McbException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def getStationsAndStatusesFromAndroidAssetFile(providerId, inputfile):
  tree = ET.parse(inputfile)
  rootNode = tree.getroot()

  stationsAndStatuses = []
  for stationNode in rootNode:
    for subNode in stationNode:
      if (subNode.tag == "id"):
        name = None
        externalId = subNode.text
      elif (subNode.tag == "description"):
        description = subNode.text
      elif (subNode.tag == "longitude"):
        longitude = subNode.text
      elif (subNode.tag == "latitude"):
        latitude = subNode.text
    stationStatus = StationStatus(None, None, "0", None, None, None, None)
    stationsAndStatuses.append(StationAndStatus(providerId, externalId, name, description, latitude, longitude, stationStatus, datetime.utcnow()))
  return stationsAndStatuses

def updateStationAndStatuses(providerId, inputFile):
  stationAndStatuses = getStationsAndStatusesFromAndroidAssetFile(providerId, inputFile)
  MyCityBikes.putStationAndStatuses(providerId, stationAndStatuses)

def __usage():
  print "USAGE: " + sys.argv[0] + " providerId assetfilepath"
  print "\tproviderId\tthe id of the provider that manages the stations"
  print "\tassetfilepath\tthe path of the file containing the android client XML assets"

if __name__ == "__main__":
  import sys
  if (len(sys.argv) < 2):
    print "ERROR: Missing providerId argument"
    __usage()
    exit()
  if (len(sys.argv) < 3):
    print "ERROR: Missing input filepath argument"
    __usage()
    exit()

  providerId = sys.argv[1]
  inputFile = sys.argv[2]

  updateStationAndStatuses(providerId, inputFile)
