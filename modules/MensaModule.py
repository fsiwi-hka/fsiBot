#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule


import urllib2
import unicodedata
from BeautifulSoup import BeautifulSoup

import os, sys, re, time

def toFloat(s):
	f = 0.0
	try:
		f = float(s)
	except:
		do = 'nothing?'
	return f
	

def toInt(s):
	f = 0
	try:
		f = int(s)
	except:
		do = 'nothing?'
	return f
	
#TODO: Need a Regex here?
def formatString(str):
	while str.count("  ") != 0:
		str = str.replace("  ", " ")
	return str

class MensaModule(BotModule):
	def __init__(self):
		self.lastFetch = 0
		self.cache = None
		return

	def getMeals(self):
		if self.cache != None and (self.lastFetch + 60.0*60.0) > time.time():
			return self.cache
	
		url = "http://www.studentenwerk-karlsruhe.de/de/essen/?view=ok&STYLE=popup_plain&c=moltke"

		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
		soup = BeautifulSoup(str(soup.body.table))

		days = soup.findAll("table", {"width" : "700"})

		mensa = []

		dayNumber = 0
		for day in days:
			linenames = []
			for line in day.findAll("td", {"width" : "20%"}):
				s = line.find(text=True)
				s = unicodedata.normalize('NFD', s).encode('utf-8','replace')
				linenames.append(str(s))

			meals = []
			for i in range(len(linenames)):
				meals.append([])

			linenumber = 0
			for meal in day.findAll("table"):
				for foo in meal.findAll("tr"):
					description = foo.findAll(text=True)
					s = ''.join(description).replace("\n"," ").replace("&euro;", "Eur")
					s = unicodedata.normalize('NFD', s).encode('utf-8','replace')
					meals[linenumber].append(formatString(str(s)))
				linenumber = linenumber + 1
			
			dayNumber = dayNumber + 1
			mensa.append([linenames, meals])
		self.cache = mensa
		self.lastFetch = time.time()
		return mensa

	def command(self, nick, cmd, args, type):
		if cmd == "!mensa":
			try:
				dayOffset = 0
				if len(args) == 1:
					time = args[0].lower()
					if time == "heute" or time == "today":
						dayOffset = 0
					elif time == "morgen" or time == "tomorrow":
						dayOffset = 1
					elif time == "übermorgen" or time == "uebermorgen":
						dayOffset = 2
					else:
						dayOffset = toInt(args[0])

				if dayOffset < 0 or dayOffset >= 5:
					self.sendPrivateMessage(nick, "Mensa: Fehler, Tagesoffset ausserhalb der gültigen Reichweite. Fixme?")
					return

				empty = True
				meals = self.getMeals()
				for i in range(len(meals[dayOffset][0])):
					send = False
					line = "[" + meals[dayOffset][0][i] + "]" + ""
					for f in range(len(meals[dayOffset][1][i])):
						price = 0.0
						currentMeal = meals[dayOffset][1][i][f]
						r = re.compile("(\d+,\d\d) E")
						prices = r.findall(currentMeal)
						if(len(prices) == 1):
							price = toFloat(prices[0].replace(",","."))
						if price > 1.0:
							send = True
							if f != 0:
								line = line + " - "
							line = line + currentMeal
					if send:
						self.sendPublicMessage(line)
						empty = False
				if empty:
					self.sendPrivateMessage(nick, "Keine Gerichte gefunden.")
			except:
				self.sendPrivateMessage(nick, "Exception returned. Fixme!")
				

	def help(self, nick):
		self.sendPrivateMessage(nick, "!mensa [offset] - Mensaplan der laufenden Woche. offset = [0-9] oder 'heute'/'morgen', default 'heute'")
		return
