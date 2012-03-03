#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, re

class LinkModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!l" or cmd == "!link":

			links = open(os.path.abspath(os.path.dirname(sys.argv[0])) + "/links", "r")
			if len(args) != 0:
				reg = re.compile('\^\W*(' + args[0] + ')\W*\|\W*([^\|]*?)\|', re.IGNORECASE)
			else:
				reg = re.compile('\^\W*([^\|]*)\W*\|\W*([^\|]*?)\|', re.IGNORECASE)

			if len(args) == 0:
				self.sendPrivateMessage(nick, 'Folgende URLs sind bekannt und können per !link <name> gepostet werden:')
				# Just output all known links
				for line in links:
					link = reg.match(line)
					if link:
						self.sendPrivateMessage(nick, link.group(1) + ': ' + link.group(2))
				return

			# Fetch entry in table
			for line in links:
				link = reg.match(line)
				if link:
					self.sendPublicMessage(link.group(2))

	def help(self, nick):
		self.sendPrivateMessage(nick, "!link/!l [link label] - Gibt eine bestimmte URL aus. (http://hska.info/links).")
		return
