from utils import *

from mycitybikes_stockholm_clearchannel import *

class test:

  def setUp(self):
    self.old_httplib2 = httplib2.Http
    httplib2.Http = MyHttpReplacement

  def tearDown(self):
    httplib2.Http = self.old_httplib2


  def test_getStationsAndStatusesFromAndroidAssetFile(self):
    stationsAndStatuses = getStationsAndStatusesFromAndroidAssetFile("5", "./assets/stockholm.xml")
    assert len(stationsAndStatuses) == 72
    assert stationsAndStatuses[0].latitude == "59.314224"
    # etc...
