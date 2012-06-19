import urllib2
import json 
#import sqlite3
import math
import time
import Queue as Q


'''
Challenges:
	- The very nearest, based on distance from lat/lng data, bus stop to a location
	is not necessarily the correct bus stop to walk to for the optimal trip to the end
	location, need to possibly consider the 2nd or 3rd nearest etc...
	- A* search seems to be the best way to find the fastest combination of bus routes
	- Choice of heuristic: possibilities include total time so far or distance from destination,
	current number of buses taken, etc... It would probably be best to combine these in some way
	in order to minimize both trip time, number of buses take, and fare cost.

	- combine walking time with travel time on the buses for heuristics, this probably
	will solve the problem of the absolute nearest stop to the final location, not being the
	ideal stop to end at 

	- End of routes seem to present the problem that, bustracker data does not list a bus
	as actually stopping at it's final stop 



Notes:
	- All bus stops list the next three times during the day, so the list that stop_times
	returns will have a length that is divisible by 3 unless it is near the end of the day
	and there will not be three more runs, need to account for this eventually, probably by 
	caching the end of day times and checking current local time against end of day time to 
	determine the number of buses that will be listed

	- Need a list of bus stops, sorted by bus route, and routes need to be differentiated
	by inbound/outbound 3c/n etc...

'''


# Calculate distance between two points given lattitude and longitude coordinates
def distance_lat_lon(p1,p2):
	earth_rad = 6378.1 # kilometers
	lat1 = p1[0]
	lat2 = p2[0]
	lon1 = p1[1]
	lon2 = p2[1]
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	psi1 = math.radians(lon1)
	psi2 = math.radians(lon2)

	d = 2*earth_rad * math.asin(math.sqrt(math.sin((phi2-phi1)/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin((psi2-psi1)/2)**2))
	return d


google_geocode_api = 'http://maps.googleapis.com/maps/api/geocode/json?address=INPUT&sensor=false'

average_walking_speed = 5.0 # kilometers/hour


raw_stops = [line.strip().split('*') for line in open('stops_lat_lon.txt').readlines()]
stops_gps = {}
stops_id = {}
stops_dist_map = {}

# Build dictionaries to store stop information, one sorted by GPS data
# the other by stop id number
for line in raw_stops:
	stops_id[line[0]] = (line[1],(line[2],line[3]))
	stops_gps[(line[2],line[3])] = (line[0],line[1])

# loading this data makes startuo time very slow, probably best to eventually store
# all of it in some sort of database or something that can be read in more efficiently
# even storing it in a text file would probably speed up the start time significantly
for stop in stops_id:
	stops_dist_map[stop] = {}
	for stop1 in stops_id:
		p1 = stops_id[stop][1]
		p1 = (float(p1[0]),float(p1[1]))
		p2 = stops_id[stop1][1]
		p2 = (float(p2[0]),float(p2[1]))
		stops_dist_map[stop][stop1] = distance_lat_lon(p1,p2)


'''
I want this to return a list, possibly of pairs, of the valid ordering
of bus stops and routes to take from start to end 

Current assumption is that a person wouldn't want to walk more than
2 kilometers from a given bus stop or start/end point, providing a radius
argument will adjust this is someone is willing to walk more or less to get
to a bus stop

using A* search with cost function f(x)=h(x)+g(x) where in this case

h(x) = distance between current stop and end 
g(x) = time taken so far on trip from start to current stop 

Need to compute distance from end point before adding
stops on to the priority queue to determine if it might be best to just walk


'''
def shortest_trip(start, end,radius=2.0):
	pq = Q.PriorityQueue()
	for stop in stops_gps:
		dist = distance_lat_lon(start,stops_gps[stop])
		if dist <= radius:
			cost = dist/average_walking_speed
			pq.put(cost,stop)
		else:
			print "There are no nearby stops to that starting point."
			return []

def get_nearest_stop(pt):
	min_dist = None
	min_key = None
	for key in stops_gps:
		stop_pt = (float(key[0]),float(key[1]))
		current_dist = distance_lat_lon(pt,stop_pt)
		if min_dist is None:
			min_dist = current_dist
			min_key = key
		elif current_dist < min_dist:
			min_dist = current_dist
			min_key = key
	return min_key , stops_gps[min_key]




# Get an address from the user to query for lat/lon
def get_address(message):
	address = raw_input(message)
	return address.replace(' ','+')

# Get json format containing lat/lon info
def get_json(address):
	response = urllib2.urlopen(google_geocode_api.replace('INPUT',address))
	return response.readlines()

# parse lat/lon info out of xml
def json_to_lat_lon(data):
	lines = [line.strip() for line in data]
	string = ''
	for line in lines:
		string += line
	json_data = json.loads(string)
	# this gets just the lat/lng of the address
	# it is possible to get NE/SW ranges which might help for better checking rought estimates 
	# store in a database
	base = json_data[u'results'][0][u'geometry'][u'location']
	lat = base[u'lat']
	lng = base[u'lng']
	return lat,lng


def strip(html):
    state = 0
    out = ""
    for char in html:
        if char == '<':
            state = 1
        elif char == '>':
            state = 0
        if state == 0:
            if char == '>':
                out += " "
            else:
                out += char
        elif state == 1:
            pass
    return out

def stop_times(stop):
    base_url = 'http://bustracker.muni.org/InfoPoint/map/GetStopHtml.ashx?vehicleId='
    url = base_url + str(stop)
    html = urllib2.urlopen(url).read()
    stop_time_list = list(reversed(strip(html).split('    ')[::-1][1::]))[3::]
    return stop_time_list



def main():
	start = get_address("Enter start location: ")
	json_data = get_json(start)
	start_pt = json_to_lat_lon(json_data)
	end = get_address("Enter end location: ")
	json_data = get_json(end)
	end_pt = json_to_lat_lon(json_data)
	print "Distance: ", distance_lat_lon(start_pt,end_pt), "kilometers"
	start_stop = get_nearest_stop(start_pt)
	end_stop = get_nearest_stop(end_pt)
	print "Start Stop: ", start_stop[1][1]
	print "End Stop: ", end_stop[1][1]	


if __name__ == "__main__":
	main()


'''
NEED TO RECALCULATE THIS ON A DAY THAT THE 102 runs, because all 102 data is missing from 
routes

routes = {}
for stop in stops_id:
   blist = [line.split('  ')[1] for line in stop_times(stop)]
   for item in blist:
       routes[item]=item


for route in routes:
    routes[route] = []
    bus_num = convert(route.split(' ')[0])
    for stop in bus_num_stops[bus_num]:
        blist = [line.split('  ')[1] for line in stop_times(stop)]
        if route in blist:
            routes[route]+=[stop] 

def convert(n):
	if n == '3N' or n == '3C':
		return 3
	elif n == '7A':
		return 7
	else:
		return int(n)

bus_nums = [1,2,3,7,8,9,13,14,15,36,45,60,75,102]
bus_num_stops = {}

for bus in bus_nums:
    bus_num_stops[bus] = []
    stops_url = base_url+str(bus)
    response = urllib2.urlopen(stops_url)
    data = response.read()
    root = ET.fromstring(data)
    stop_list = list(list(root)[0])
    for stop in stop_list:
        bus_num_stops[bus]+=[stop.attrib['html']]

Also need to recalculate: 
	- number_to_routes.json
	- route_stops.json 


'''







