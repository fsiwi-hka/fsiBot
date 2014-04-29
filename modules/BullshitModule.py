#! /usr/bin/env python

from BotModule import BotModule
import urllib2

class BullshitModule(BotModule):
	def __init__(self):
		pass

	def command(self, nick, cmd, args, type):
		if type == "public" and (cmd == "!bs" or cmd == "!klaus"):
			ht = urllib2.urlopen("http://bullshit.aiju.de")
			for i in range(0, 6):
				ht.readline()
			self.sendPublicMessage(ht.readline()[:-7])

	def help(self, nick):
		self.sendPrivateMessage(nick, "!bs - Print a stream of bullshit from http://bullshit.aiju.de")
