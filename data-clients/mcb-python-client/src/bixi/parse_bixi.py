import httplib2
import time
import datetime
from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB
import xml.etree.ElementTree as ET
import re


def xmlnode2dict(node):
  result = {}
  for subnode in node:
    children = subnode.getchildren()
    if children:
      result[subnode.tag] = xmlnode2dict(subnode)
    else:
      result[subnode.tag] = subnode.text
    
  return result

def parse_bixi(content):
  stations = ET.XML(content)
  stations = [xmlnode2dict(station) for station in stations]
  return stations
  