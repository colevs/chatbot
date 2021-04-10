from location import Location as lc
from PIL import Image

import io
import apikey
import requests
import json

API_KEY = apikey.getKey()
SIZE = '400x400'

URL1 = "https://maps.googleapis.com/maps/api/streetview?size="
URL2 = "&location="
URL3 = "&fov=80&heading=70&pitch=0&key="

class GoogleStreetViewAPI(object):
	def sendRequest(entities):
		places = entities['wit$location:location']
		location = ''
		if len(places) == 0:
			location = 'here'
		else:
			location = places[0]['value']

		locationCoords = lc.getLocation(location)
		locationCoordsString = str(locationCoords[0]) + ',' + str(locationCoords[1])

		resp = requests.get(URL1 + SIZE + URL2 + locationCoordsString + URL3 + API_KEY)

		if resp.status_code != 200:
		    print('error: ' + str(resp.status_code))
		    return None
		else:
			image_bytes = io.BytesIO(resp.content)
			img = Image.open(image_bytes)
			return img