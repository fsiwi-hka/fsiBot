#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random, commands

class FortuneModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!fortune":
			output = commands.getoutput("fortune -s").replace("\n", " ").replace("\t", " ")
			if type == "private":
				self.sendPrivateMessage(nick, output)
			else:
				self.sendPublicMessage(output)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!fortune - Glückskeks und so.")
		return
