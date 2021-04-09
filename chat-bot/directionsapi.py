from location import Location as lc

import requests
import json

API_KEY = "AIzaSyDzBqKvMiLOTM6s2z-GscqMYTwOkFjA_s0"
URL1 = "https://maps.googleapis.com/maps/api/directions/json?origin="
URL2 = "&destination="
URL3 = "&key="

class GoogleDirectionsAPI(object):
	def sendRequest(entities):
		places = entities['wit$location:location']
		origin = ''
		destination = ''
		if len(places) > 1:
			origin = places[0]['value']
			destination = places[1]['value']
		else:
			origin = 'here'
			destination = places[0]['value']

		originCoords = lc.getLocation(origin)
		originCoordsString = str(originCoords[0]) + ',' + str(originCoords[1])

		destinationCoords = lc.getLocation(destination)
		destinationCoordsString = str(destinationCoords[0]) + ',' + str(destinationCoords[1])

		resp = requests.get(URL1 + originCoordsString + URL2 + destinationCoordsString + URL3 + API_KEY)

		if resp.status_code != 200:
		    print('error: ' + str(resp.status_code))
		    return None
		else:
			response = resp.json()['routes'][0]['legs'][0]['steps']
			for step in response:
				del step['polyline']
			return response