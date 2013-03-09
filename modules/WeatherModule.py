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

			if postalcode.startswith('Honoluluu'):
				answer = 'Computer sagt: NEIN!'
				if type == 'public':
					self.sendPublicMessage(answer)
				else :
					self.sendPrivateMessage(nick, answer)
				return
			elif postalcode == 'Mele Island':
				answer = 'Dublonen, Dublonen!'
				if type == 'public':
					self.sendPublicMessage(answer)
				else :
					self.sendPrivateMessage(nick, answer)
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

			if len(jsondata['list']) < 1:
				answer = 'Leck? welches Leck?'
				if type == 'public':
					self.sendPublicMessage(answer)
				else :
					self.sendPrivateMessage(nick, answer)
				return

			elif len(jsondata['list']) > 1:
				answer = 'Mr Cotton´s Papagei! Die selbe Frage!'
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
				weather['cloudiness'] = jsondata['list'][0]['clouds']['all']
			except KeyError, e:
				if self.DEBUG:
					print "KeyError: %s" % e

			answer = "Wetter für %s: %.2f°C, %s" % (weather['city'].encode('utf-8'), weather['temp'], weather['cond'].encode('utf-8'))

			if 'windspeed' in weather:
				answer += ", wind speed: %.1fkm/h" % weather['windspeed']

			if 'humidity' in weather:
				answer += ", humidity: %d%%" % weather['humidity']

			if 'cloudiness' in weather:
				answer += ", cloudiness: %d%%" % weather['cloudiness']

			if type == 'public':
				self.sendPublicMessage(answer)

				if weather['temp'] > 30:
					self.sendPublicMessage('Willkommen in der der Karibik, *croak* Schätzchen!')
			else :
				self.sendPrivateMessage(nick, answer)


	def help(self, nick):
		self.sendPrivateMessage(nick, "!wetter [Ort] - Gibt aktuelle Wetterdaten aus. Default Ort ist Karlsruhe.")
		return
