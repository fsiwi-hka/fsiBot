#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random

# To find a needle in a haystack
def isOccuring(needle, haystack, caseInsensitive = False):
	for hay in haystack:
		if caseInsensitive:
			if needle.lower().find(hay.lower()) > -1:
				return True
		else:
			if needle.find(hay) > -1:
				return True
	return False

class BestOfModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!bo" or cmd == "!bestof":
			bofile = open(os.path.abspath(os.path.dirname(sys.argv[0])) + "/bestof", "r")

			# Fetch best of quotes.
			bo = []
			author = ""
			for line in bofile:
				if line.startswith("===="):
					author = line[5:].replace(" ====", "").replace("\n", "")
				if line.startswith("  *"):
					if len(args) == 0 or isOccuring(line, args, True) or isOccuring(author, args, True):
						bo.append('"' + line[4:].replace("\n", "") + '" -- ' + author + ', via http://hska.info/bestof')
			line = ""	
			if len(bo) == 0:
				line = "Kein passendes Best-Of gefunden."
			else:
				line = bo[random.randint(0, len(bo)-1)]

			if type == "private":
				self.sendPrivateMessage(nick, line)
			else:
				self.sendPublicMessage(line)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!bestof/!bo [Stichwort] - Zeigt eines der Best-Of Kommentare eines Profs an (http://hska.info/bestof).")
		return
