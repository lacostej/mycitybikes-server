#!/usr/bin/python

#
# Helper module to convert station assets XML files used by the original android client to the format required by the push stations REST API
#

import xml.etree.ElementTree as ET

from mycitybikes.mycitybikes import *

def getStationsFromAndroidAssetFile(inputfile, providerId):
  tree = ET.parse(inputfile)
  rootNode = tree.getroot()

  stations = []
  for stationNode in rootNode:
    for subNode in stationNode:
      if (subNode.tag == "id"):
        name = subNode.text
        externalId = subNode.text
      elif (subNode.tag == "description"):
        description = subNode.text
      elif (subNode.tag == "longitude"):
        longitude = subNode.text
      elif (subNode.tag == "latitude"):
        latitude = subNode.text
    stations.append(Station(None, providerId, externalId, name, description, latitude, longitude))
  return stations

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
  inputfile = sys.argv[2]

  stations = getStationsFromAndroidAssetFile(inputfile, providerId)

  print StationList.to_xml(stations)
