from elementtidy.TidyHTMLTreeBuilder import TidyHTMLTreeBuilder as TB
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulStoneSoup

def parse_node(node):
    
    #tb = TB()
    #tb.feed(description)
    #element = tb.close()
    #body=node.getchildren()[1][0].getchildren()
    try:
        description = node[0].text
        soup = BeautifulStoneSoup(description)
        divs = soup.findAll('div')
        name = divs[1].string
        bikes = divs[3].contents[0]
        aparcamientos = divs[3].contents[2] # TODO: find a translation and check the order    
        
        point = node[2][0].text.split(',')[:2]
        latitude, longitude = point
    except Exception, e:
        print e
        return None
    
    station = dict(name=name,
                   description=name,
                   latitude=latitude,
                   longitude=longitude)
    
    station_status = dict(online=bikes,
                          availableBikes=bikes,
                          freeSlots=bikes)
    station['stationStatus'] = station_status
    
    return station
                   
def parse_document():
    f = open('tests/data/kml.xml', 'rb')
    content = f.read()
    f.close()
    xml = ET.XML(content)
    xml = xml.getchildren()[0]
    nodes = [node for node in xml if len(node.getchildren()) == 3]
    
    nodes = [parse_node(node) for node in nodes]
    print nodes
    
if __name__ == '__main__':
    parse_document()