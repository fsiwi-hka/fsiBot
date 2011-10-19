#! /usr/bin/env python
# coding=utf8

# Baseclass of all modules, handles important stuff
class BotModule(object):
	def __init__(self):
		return

	def tick(self):
		return
	
	def setup(self, private, public, privaction, pubaction, kick, debug):
		self.sendPrivateMessage = private
		self.sendPublicMessage = public
		self.sendPrivateAction = privaction
		self.sendPublicAction = pubaction
		self.kick = kick
		self.DEBUG = debug

# An example on howto write modules
class HelloWorldExample(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!hello":
			if type == "private":
				self.sendPrivateMessage(nick, "world!")
			else:
				self.sendPublicMessage("world!")

	def help(self, nick):
		self.sendPrivateMessage(nick, "!hello - Antwortet 'world!'")
		return
