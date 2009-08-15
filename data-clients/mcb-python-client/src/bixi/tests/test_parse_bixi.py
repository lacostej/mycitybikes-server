import urlparse
import httplib2
import os
import parse_bixi
from email import message_from_string, message_from_file
HTTP_SRC_DIR = "./data/"

class MyHttpReplacement:
  """Build a stand-in for httplib2.Http that takes its response headers and bodies from files on disk"""

  def __init__(self, cache=None, timeout=None):
    self.hit_counter = {}

  def request(self, uri, method="GET", body=None, headers=None, redirections=5):
    path = urlparse.urlparse(uri)[2]
    fname = os.path.join(HTTP_SRC_DIR, path[0:])
    f = open(fname,'rb')
    if not os.path.exists(fname):
      index = self.hit_counter.get(fname, 1)
      if os.path.exists(fname + "." + str(index)):
        self.hit_counter[fname] = index + 1
        fname = fname + "." + str(index)
    if os.path.exists(fname):
      f = file(fname, "r")
      response = message_from_file(f)
      f.close()
      body = response.get_payload()
      headers = httplib2.Response(response)
      print body
      return (headers, body)
    else:
      return (httplib2.Response({"status": "404"}), "")

  def add_credentials(self, name, password):
    pass

def setUp():
  old_httplib2 = httplib2.Http
  httplib2.Http = MyHttpReplacement

def tearDown():
  httplib2.Http = self.old_httplib2
  
def testParseBixi():
  setUp()
  url = 'bixi.xml'
  h = httplib2.Http(".cache")
  resp, content = h.request(url)
  if (resp.status != 200):
    raise Exception("couldn't open url " + url)
  if (resp['content-type'] != 'text/xml'):
    raise Exception("Invalid content-type")
  try:
   result = parse_bixi.parse_bixi(content)
  except:
    raise Exception("Invalid XML file")
  assert len(result) == 300
  assert result[0]['nbBikes'] == 4
  assert result[-1]['name'] == '8dsupporttech1'
if __name__ == "__main__":
  testParseBixi()
  