#! /usr/bin/env python
# coding=utf8
from BotModule import BotModule

import urllib, json

class WeatherModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!wetter":
			postalcode = "Karlsruhe"
			if len(args) > 0:
				postalcode = ' '.join(args)

			if postalcode.startswith('Honoluluuu'):
				self.sendPublicMessage('Computer sagt: NEIN!')
				return

			try:
				u = urllib.urlopen("http://api.openweathermap.org/data/2.1/find/name?q=%s&type=like&units=metric" % urllib.quote(postalcode))
			except urllib2.HTTPError, e:
				if self.DEBUG:
					print 'Error fetching data, Error: %s' % e.code
				return
			except urllib2.URLError, e:
				if self.DEBUG:
					print 'Error fetching data, Error: %s' % e.args
				return

			if u.getcode() != 200:
				if self.DEBUG:
					print 'Error fetching data, Errorcode: %s' % u.getcode()
				return

			try:
				jsondata = json.loads(u.read())
			except ValueError, e:
				if self.DEBUG:
					print "ValueError %s" % e
				return

			if jsondata['cod'] != '200':
				if jsondata['message'] != '':
					answer = jsondata['message'].encode('utf-8')
					if type == 'public':
						self.sendPublicMessage(answer)
					else :
						self.sendPrivateMessage(nick, answer)
				return

			weather = {}
			try:
				weather['city'] = jsondata['list'][0]['name']
				weather['temp'] = jsondata['list'][0]['main']['temp']
				weather['cond'] = jsondata['list'][0]['weather'][0]['description']
				weather['humidity'] = jsondata['list'][0]['main']['humidity']
				weather['windspeed'] = jsondata['list'][0]['wind']['speed']
			except KeyError, e:
				weather[e] = False
				if self.DEBUG:
					print "KeyError: %s" % e

#			humi = root.find(".//humidity").attrib["data"].encode("utf-8")
#			wind = root.find(".//wind_condition").attrib["data"].encode("utf-8")

			answer = "Wetter für %s: %.2f °C, %s" % (city.encode('utf-8'), temp, cond.encode('utf-8'), windspeed, humidity)

			if weather['windspeed'] is not None:
				answer += ", wind speed: %.1f" % weather['windspeed']

			if weather['humidity'] is not None:
				answer += ", humidity: %d" % weather['humidity']

			if type == 'public':
				self.sendPublicMessage(answer)
			else :
				self.sendPrivateMessage(nick, answer)

#			self.sendPrivateMessage(nick, humi)
#			self.sendPrivateMessage(nick, wind)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!wetter [Ort] - Gibt aktuelle Wetterdaten aus. Default Ort ist Karlsruhe.")
		return
