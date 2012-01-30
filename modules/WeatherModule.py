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

			if root.find(".//problem_cause") is not None:
				print "[WeatherModule] Error: " + root.find(".//problem_cause").attrib["data"]
			else:
				city = root.find(".//city").attrib["data"].encode("utf-8")
				temp = root.find(".//temp_c").attrib["data"].encode("utf-8")
				cond = root.find(".//condition").attrib["data"].encode("utf-8")
				humi = root.find(".//humidity").attrib["data"].encode("utf-8")
				wind = root.find(".//wind_condition").attrib["data"].encode("utf-8")

				self.sendPrivateMessage(nick, "Wetter für " + city + ":")
				self.sendPrivateMessage(nick, temp + "°C, " + cond)
				self.sendPrivateMessage(nick, humi)
				self.sendPrivateMessage(nick, wind)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!wetter [Ort] - Gibt aktuelle Wetterdaten aus. Default Ort ist Karlsruhe.")
		return
