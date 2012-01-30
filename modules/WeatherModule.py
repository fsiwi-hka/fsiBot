#! /usr/bin/env python
# coding=utf8

# Geklaut bei qchn.

from BotModule import BotModule

from time import *

import os, sys, random
import urllib
import lxml.etree

class WeatherModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!wetter":
			postalcode = "Karlsruhe"
			if len(args) > 0:
				postalcode = ' '.join(args)
			raw = urllib.urlopen("http://www.google.com/ig/api?weather=%s&hl=de" % urllib.quote(postalcode)).read()
			data = unicode(raw, "latin1")
			root = lxml.etree.fromstring(data).getroottree()

			city = root.find(".//city").attrib["data"]
			temp = root.find(".//temp_c").attrib["data"]
			cond = root.find(".//condition").attrib["data"]
			humi = root.find(".//humidity").attrib["data"]
			wind = root.find(".//wind_condition").attrib["data"]

			self.sendPrivateMessage(nick, "Wetter für " + city.encode("utf-8") + ":")
			self.sendPrivateMessage(nick, temp + "°C, " + cond)
			self.sendPrivateMessage(nick, humi.encode("utf-8"))
			self.sendPrivateMessage(nick, wind)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!wetter - Gibt aktuelle Wetterdaten aus.")
		return
