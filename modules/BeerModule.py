#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

from time import *

import os, sys, random

class BeerModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		lt = localtime()	
		if type == 'public' and (cmd == "!beer" or cmd == "!bier"):
			if 6 < lt[3] < 16:
				line = "Kein Bier vor 4!"
				self.sendPublicMessage(line)
			else:
				schmack = random.choice(["leckeres", "wohltuendes", "wohlschmeckendes", "eisgekühltes", "lauwarmes", "abgestandenes", "schales"])
				beer = random.choice(["Tannenzäpfle", "Höpfner", "Leikeim", "Becks", "Jever", "Öttinger", "Palmbräu", "Andechser Doppelbock", "Kölsch", "Veltins"])
				
				compliment = ""
				reciever = nick
				if len(args) > 0:
					reciever = args[0]
					compliment = " Mit freundlichen Grüßen von " + nick
				line = "gibt " + reciever + " ein " + schmack + " " + beer + "." + compliment

				self.sendPublicAction(line)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!bier/!beer - Verteilt Bier.")
		return
