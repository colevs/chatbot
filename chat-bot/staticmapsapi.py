from location import Location as lc
from PIL import Image

import io
import apikey
import requests
import json

API_KEY = apikey.getKey()
ZOOM_LEVEL = '12'
SIZE = '400x400'

URL1 = "https://maps.googleapis.com/maps/api/staticmap?center="
URL2 = "&zoom="
URL3 = '&size='
URL4 = '&key='

class GoogleStaticMapsAPI(object):
	def sendRequest(entities):
		places = entities['wit$location:location']
		location = ''
		if len(places) == 0:
			location = 'here'
		else:
			location = places[0]['value']

		locationCoords = lc.getLocation(location)
		locationCoordsString = str(locationCoords[0]) + ',' + str(locationCoords[1])

		resp = requests.get(URL1 + locationCoordsString + URL2 + ZOOM_LEVEL + URL3 + SIZE + URL4 + API_KEY)

		if resp.status_code != 200:
		    print('error: ' + str(resp.status_code))
		    return None
		else:
			image_bytes = io.BytesIO(resp.content)
			img = Image.open(image_bytes)
			return img