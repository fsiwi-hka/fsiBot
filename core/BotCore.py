#! /usr/bin/env python
# coding=utf8

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

import os, sys, random, time

class FSIBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667, debug=False):
		self.DEBUG = debug
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

		self.connection.add_global_handler("join", getattr(self, "inform_webusers"), 42)

		for i in ["kick", "join", "quit", "part", "topic", "endofnames", "notopic"]:
			self.connection.add_global_handler(i, getattr(self, "dump_users"), 42)

		# We need to distinguish between private and public messages
		self.connection.add_global_handler("pubmsg", getattr(self, "publicMessage"), 42)
		self.connection.add_global_handler("privmsg", getattr(self, "privateMessage"), 42)

		# Initialize module lists
		self.modules = []
		

	def on_nicknameinuse(self, c, e):
		#c.nick(c.get_nickname() + "_")
		#sendPrivateMessage("nickserv", "ghost fsibot FOO")
		#time.sleep(3)
		#c.nick(c.get_nickname())
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		#self.sendPrivateMessage("nickserv", "identify FOO")
		c.join(self.channel)

	def on_all_raw_messages(self, c, e):
		if self.DEBUG:
			print str(e.eventtype()) + " " + str(e.source()) + " " + str(e.target()) + " " + str(e.arguments())

	#todo: Maybe we dont need these functions, look into the handler
	def publicMessage(self, c, e):
		self.parseMessage(c, e, 'public')

	#todo: same as above
	def privateMessage(self, c, e):
		self.parseMessage(c, e, 'private')

	# Sends a private message ("query") to nick
	def sendPrivateMessage(self, nick, message):
		self.connection.privmsg(nick, message)

	# Sends a public message to the bots channel
	def sendPublicMessage(self, message):
		self.connection.privmsg(self.channel, message)

	def sendPrivateAction(self, nick, message):
		self.connection.action(nick, message)

	def sendPublicAction(self, message):
		self.connection.action(self.channel, message)

	# Adds a module to the module list
	def addModule(self, module):
		module.setup(self.sendPrivateMessage, self.sendPublicMessage, self.sendPrivateAction, self.sendPublicAction, self.DEBUG)
		self.modules.append(module)

	# type: 'public', 'private'
	def parseMessage(self, c, e, type):
		nick = nm_to_n(e.source())
		
		# Splitting the string into command and arguments
		args = e.arguments()[0].split()

		# Check if message is empty
		if len(args) == 0:
			return

		cmd = args[0].lower()
		args.pop(0)

		if self.DEBUG:
			print "Parsing " + str(type) + " command '" + str(cmd) + "' with '" + str(args) + "' from '" + str(nick) + "'"

		# User requested help. Send introduction string, then all help strings from all modules
		# Also, hardcoded strings.
		if cmd == "!help":
			self.sendPrivateMessage(nick, "Hallo " + nick + ", ich bin der Bot der Fachschaft Informatik. Hier sind meine Befehle:")
			self.sendPrivateMessage(nick, "!kontakt - Zeigt dir Kontaktinformationen zur Fachschaft an.")	
			for module in self.modules:
				module.help(nick)
			return

		# A few hardcoded commands that don't really need to be a module right now
		if cmd == "!kontakt":
			self.sendPrivateMessage(nick, "E-Mail: kontakt@hska.info :: Tel: 0721 925-1448")
			return
		
		# every string that starts with an '!' is considered to be an command
		if cmd.startswith("!"):
			for module in self.modules:
				module.command(nick, cmd, args, type)

	# Dumps the number of chat users to a logfile
	def dump_users(self, c, e):
		users = 0
		for chname, chobj in self.channels.items():
			users = users + len(chobj.users())

		users = users - 1

		userfile = open(os.path.abspath(os.path.dirname(sys.argv[0])) + "/users.log", "w")
		userfile.write(str(users))
		userfile.close()
		print "Updated userfile to " + str(users) + " users"

	# Sends information string to webchat users coming from our site
	def inform_webusers(self, c, e):
		nick = nm_to_n(e.source())
		if nick.startswith("fsiWeb"):
			c.privmsg(nick, "Wenn du dich auf der Fachschaftsseite anmeldest, kannst du in deinen Einstellungen einen Nick für den Webchat festlegen.")
