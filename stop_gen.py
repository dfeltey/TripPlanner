import xml.etree.ElementTree as ET
import urllib2
import sqlite3



#conn = sqlite3.connect("stops.db")

routes = [1,2,3,7,8,9,13,14,15,36,45,60,75,102]
base_url = "http://bustracker.muni.org/InfoPoint/map/GetRouteXml.ashx?RouteId="
stops_txt = open('stops_lat_lon.txt','w')

stops = {}

for route in routes:
	stops_url = base_url + str(route)
	response = urllib2.urlopen(stops_url)
	data = response.read()
	root = ET.fromstring(data)
	stop_list = list(list(root)[0])

	for stop in stop_list:
		stops[stop.attrib['html']] = stop.attrib['html']+'*'+stop.attrib['label']+'*'+stop.attrib['lat']+'*'+stop.attrib['lng']+'\n'


for stop in stops:
	stops_txt.write(stops[stop])

