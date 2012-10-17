#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random, commands

class FortuneModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!fortune":
			fargs = "-s"
			if len(args) >= 1:
				if args[0] == "bofh":
					fargs = "bofh-excuses"
				if args[0] == "offensive":
					fargs = "-s -o"

			output = commands.getoutput("fortune " + fargs).replace("\n", " ").replace("\t", " ")
			if type == "private":
				self.sendPrivateMessage(nick, output)
			else:
				self.sendPublicMessage(output)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!fortune - Glückskeks und so.")
		return
