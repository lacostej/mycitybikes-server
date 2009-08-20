from mycitybikes.mycitybikes import *
from datetime import *
import httplib2
import xml.etree.ElementTree as ET
from StringIO import StringIO
from xml.dom.minidom import Document
from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB

def dict_to_xml(dct, node_name):
  doc = Document()
  node = doc.createElement(unicode(node_name, 'utf-8'))
  for k,v in dct.items():
    if isinstance(v,dict):
      e = dict_to_xml(v, k)
    else:
      e = doc.createElement(unicode(k))
      e.appendChild(doc.createTextNode(unicode(v)))
    node.appendChild(e)
  return node

def xmlnode2dict(node):
  result = {}
  for subnode in node:
    children = subnode.getchildren()
    if children:
      result[subnode.tag] = xmlnode2dict(subnode)
    else:
      result[subnode.tag] = subnode.text
  return result

def dict_from_keys(dct, dictkeys):
  result = {}
  for newkey, oldkey in dictkeys.iteritems():
    result[newkey] = dct.get(oldkey, '')
  return result

def tofloat(value):
  try:
    return float(value)
  except:
    return float(0)