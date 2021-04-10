import re
from PIL import Image

# this class is responsible for formatting the data requested as a string that can be used as a response by the chat bot
# each function here takes in the returned data of its corresponding data request function, as well as the full list of entities
# it returns a string that the bot should respond with

class ResponseFormat(object):
	def getDistanceFormat(distance, entities):
		entities = entities['wit$location:location']
		place1 = entities[0]['value']
		if len(entities) == 1:
			return "The distance to " + place1 + " is " + str(round(distance, 2)) + "km.\n"
		else:
			place2 = entities[1]['value']
			return "The distance between " + place1 + " and " + place2 + " is " + str(round(distance, 2)) + "km.\n"

	def getTimezoneFormat(timezone, entities):
		entities = entities['wit$location:location']
		place = entities[0]['value']
		return "The time zone at " + place + " is " + str(timezone[0]) + ".\n"

	def getLocalTimeFormat(time, entities):
		entities = entities['wit$location:location']
		response = ""
		i = 0
		for location in entities:
			response += "The time in " + location['value'] + " is " + str(time[i]) + ".\n"
			i = i + 1
		return response

	def getTimeDifferenceFormat(time, entities):
		entities = entities['wit$location:location']
		if len(entities) == 1:
			return "The difference in time from here to " + entities[0]['value'] + " is " + str(time) + ".\n"
		else:
			return "The difference in time between " + entities[0]['value'] + " and " + entities[1]['value'] + " is " + str(time) + ".\n"

	def getTemperatureFormat(temps, entities):
		entities = entities['wit$location:location']
		response = ""
		i = 0
		for location in entities:
			response += "The temperature in " + location['value'] + " is " + str(temps[i]['temp']) + " degrees celcius.\n"
			i = i + 1
		return response

	def getWeatherFormat(weather, entities):
		entities = entities['wit$location:location']
		return "The weather in " + entities[0]['value'] + " is " + str(weather) + ".\n"

	def getPointOfInterestFormat(POI, entities):
		entities = entities['wit$location:location']
		response = "The POIs in " + entities[0]['value'] + " are "
		for poi in POI:
			stringsplitpoint = poi.find(', ') + 2
			response += poi[stringsplitpoint:poi.find(',', stringsplitpoint+1)] + ", "
		response = response[:-2]
		response += ".\n"
		return response

	def getStaticMapsFormat(img, entities):
		places = entities['wit$location:location']
		location = ''
		if len(places) == 0:
			location = 'here'
		else:
			location = places[0]['value']

		response = 'Here is the map I found for ' + location + '\n'
		img.show()
		return response

	def getStreetViewFormat(img, entities):
		places = entities['wit$location:location']
		location = ''
		if len(places) == 0:
			location = 'here'
		else:
			location = places[0]['value']

		response = 'Here is the street view I found for ' + location + '\n'
		img.show()
		return response

	def getDirectionsFormat(directions, entities):
		places = entities['wit$location:location']
		origin = ''
		destination = ''

		if len(places) > 1:
			origin = places[0]['value']
			destination = places[1]['value']
		else:
			origin = 'here'
			destination = places[0]['value']

		response = "The directions from " + origin + " to " + destination + " are as follows:\n"
		for step in directions:
			instructions = ResponseFormat.cleanhtml(step['html_instructions'])
			if 'maneuver' in step:
				response += instructions + '\n'
			else:
				response += instructions + ' for ' + step['distance']['text'] + '\n'

		return response

	def cleanhtml(raw_html):
		cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext