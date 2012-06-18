import xml.etree.ElementTree as ET
import json
import urllib2
import math
import time
from trip_planner import strip 

# Probably need to refactor this code, and move often used functions into a common module
# that can be imported from any of these files since strip doesn't really belong in 
# realtime_bus.py or trip_planner.py


vehicle_base_url = 'http://bustracker.muni.org/InfoPoint/map/GetVehicleXml.ashx?RouteId='
vehicle_status_base_url = 'http://bustracker.muni.org/InfoPoint/map/GetVehicleHtml.ashx?vehicleId='

def get_route_vehicles(route):
	vehicles = {}
	route_vehicle_url = vehicle_base_url+str(route)
	response = urllib2.urlopen(route_vehicle_url)
	data = response.read()
	root = ET.fromstring(data)
	for item in root:
		vehicles[item.attrib['name']]=(item.attrib['lat'],item.attrib['lng'])

	return vehicles

'''
Should probably add some exception handling to this to deal with the fact
that the data is not always returned correctly by the website...
'''
def get_vehicle_status(vehicle):
	vehicle_status_url = vehicle_status_base_url + str(vehicle)
	response = urllib2.urlopen(vehicle_status_url)
	data = response.read()
	parsed = strip(data).strip().split('  ')
	route = parsed[1].split(',')[1].split(':')[1] #.strip() ?? currently leaves space before route name
	status = parsed[4]
	recent_stop = parsed[5].split(':')[1].strip()
	direction = parsed[6].split(':')[1].strip()


	return vehicle, route, status, recent_stop, direction



