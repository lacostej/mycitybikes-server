from utils import *

from mycitybikes_montreal_bixi import *

class test:

  def setUp(self):
    self.old_httplib2 = httplib2.Http
    httplib2.Http = MyHttpReplacement

  def tearDown(self):
    httplib2.Http = self.old_httplib2


  def test_getStationsAndStatuses(self):
    Bixi.montrealStationsUrl = "/bixi_montreal_fr.xml"
    #print getBixiStationsXml()
    #stationsAndStatuses = getStationsAndStatuses("5")
    #assert len(stationsAndStatuses) == 300
#    assert stationsAndStatuses[0].latitude == "59.314224"
    # etc...
