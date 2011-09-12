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
				if len(args) > 0:
					line = "gibt " + args[0] + " ein leckeres Tannenzäpfle."
					self.sendPublicAction(line)
					line = "Geht auf " + nick + "!"
					self.sendPublicMessage(line)
					return
				else:
					line = "gibt " + nick + " ein leckeres Tannenzäpfle."
					self.sendPublicAction(line)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!beer - Verteilt Bier.")
		return
