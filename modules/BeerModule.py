#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

from time import *

import os, sys, random

class BeerModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		lt = localtime();
		if cmd == "!beer" and type != "private":
			if lt[3] > 6 and lt[3] < 16:
				line = "Kein Bier vor 4!"
				self.sendPublicMessage(line)
			else:
				schmack = random.choice(["leckeres", "wohltuendes", "wohlschmeckendes", "eisgekühltes", "lauwarmes", "abgestandenes", "schales"])
				beer = random.choice(["Tannenzäpfle", "Höpfner", "Leikeim", "Becks", "Jever", "Öttinger", "Palmbräu", "Andechser Doppelbock", "Kölsch", "Veltins"])

				line = "gibt " + nick + " ein " + schmack + " " + beer + "."
				if len(args) > 0:
					line = line + " Mit freundlichen Grüßen von " + args[0]
				self.sendPublicAction(line)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!beer - Verteilt Bier.")
		return
