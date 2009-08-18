from google.appengine.ext import webapp, db
import datetime
import types
import os
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext.db import polymodel
from xml.dom.minidom import Document
from ragendja.dbutils import get_object_or_404, to_json_data


"""Convert a dictionary to string"""
def dct_to_str(dct):
  aux = []
  for key, value in dct.iteritems():
    aux.append('%s:%s' % (key,value))
  return '{ ' + ', '.join(aux) + ' }'



def contains_keys(dct, keys):
  for key in keys:
    if not dct.has_key(key):
      return False
  return True

"""Convert an xml node to dict"""
def xmlnode2dict(node):
  result = {}
  for subnode in node:
    children = subnode.getchildren()
    if children:
      result[subnode.tag] = xmlnode2dict(subnode)
    else:
      result[subnode.tag] = subnode.text
    
  return result
    
    
def obj2dict(obj, properties, exclude=None, extra={}):
  """properties must be a dict or a list"""
  if exclude:
    if isinstance(properties, dict):
      properties = properties.keys()
    properties = set(properties) - set(exclude)
  result = to_json_data(obj, properties)
  result.update(extra)
  return result

def object_to_xml(obj, root_name=''):
  doc = Document()
  if hasattr(obj, '__iter__'):
    root_node = doc.createElement(unicode(root_name))
    for e in obj:
      root_node.appendChild(e.to_xml())
  else:
    root_node = obj.to_xml()
  doc.appendChild(root_node)
  return doc

def delete_keys(dct, keys):
  for key in keys:
    if dct.has_key(key):
      del(dct[key])

def model_to_dict(obj):
  result = dict([(key, getattr(obj, key)) for key in obj.properties()])
  result['id'] = obj.key().id()
  del(result['_class'])
  return result

def dict_to_xml(dct, node_name):
  doc = Document()
  node = doc.createElement(unicode(node_name))
  for k,v in dct.items():
    e = doc.createElement(unicode(k))
    e.appendChild(doc.createTextNode(unicode(v)))
    node.appendChild(e)
  return node

def flatten(obj, depth=0):
  """
    Thank you to the author at http://python-rest.googlecode.com for this.
    It was licensed as Apache v 2, so please use with care.

    Recursively flattens objects to a serializable form:
        datetime.datetime -> iso formatted date string
        db.users.User -> user nickname
        db.GeoPt -> string
        db.IM -> string
        db.Key -> string

    Returns:
        A shallow copy of the object

    Reference:
        http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html
        http://python-rest.googlecode.com

    """
  if isinstance(obj, datetime.datetime):
    return obj.isoformat()

  elif isinstance(obj, db.users.User):
    return obj.nickname()

  elif isinstance(obj, (db.IM, db.Key)):
    print obj
    return str(obj)

  elif isinstance(obj, GeoPt):
    return {'lat':obj.lat, 'lon':lon}

  elif isinstance(obj, types.ListType):
    return [flatten(item, depth+1) for item in obj]

#    elif isinstance(obj, (types.DictType, app3.Resource)):
#        copy = {}
#        for key in obj:
#            copy[key] = flatten(obj[key], depth+1)
#        return copy

  elif isinstance(obj, db.Model): # If it is a model, go down one level:
    return dict([(key, getattr(obj, key)) for key in obj.properties()])
  elif isinstance(obj, polymodel.PolyModel): # If it is a model, go down one level:
    return dict([(key, getattr(obj, key)) for key in obj.properties()])
  else:
    print type(obj)

    return '%s %s' % (type(obj),obj)