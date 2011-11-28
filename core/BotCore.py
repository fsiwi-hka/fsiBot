#! /usr/bin/env python
# coding=utf8

import BotModule
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

import os, sys, pyclbr, random, time, datetime, itertools

def timestamp():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

class FSIBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, password, server, port=6667, debug=False):
		self.log("Bot initialized.")
		self.DEBUG = debug
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel
		self.nick = nickname
		self.nickpassword = password
		self.connection.add_global_handler("join", getattr(self, "inform_webusers"), 42)

		for i in ["kick", "join", "quit", "part", "topic", "endofnames", "notopic"]:
			self.connection.add_global_handler(i, getattr(self, "dump_users"), 42)

		# We need to distinguish between private and public messages
		self.connection.add_global_handler("pubmsg", getattr(self, "publicMessage"), 42)
		self.connection.add_global_handler("privmsg", getattr(self, "privateMessage"), 42)
		self.connection.add_global_handler("privnotice", getattr(self, "privateMessage"), 42)
		self.connection.add_global_handler("notice", getattr(self, "privateMessage"), 42)

		# List of active modules
		self.activeModules = []
	
	def log(self, string):
		print timestamp() + ": " + string
		return

	def start(self):
		self.log("Connecting to " + self.server_list[0][0] + ":" + str(self.server_list[0][1]))
		try:
			self._connect()
			while 1:
				self.ircobj.process_once(timeout=0.2)
				
				tick = False
				for chname, chobj in self.channels.items():
					if chname == self.channel:
						tick = True

				if tick:
					for mod in self.activeModules:
						mod.tick()
                
		except KeyboardInterrupt:
			self.log("^C caught")
			self.connection.disconnect("^C caught")
			sys.exit(0)

	def on_nicknameinuse(self, c, e):
		if self.nickpassword != "":
			c.nick(c.get_nickname() + "_")
			time.sleep(2)
			sendPrivateMessage("nickserv", "ghost " + self.nick + " " + self.nickpassword)
			time.sleep(2)
			c.nick(self.nick)
			time.sleep(2)
			self.identify()
		else:
			c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		if self.nickpassword != "":
			self.identify()

		self.log("Joining channel " + self.channel)
		c.join(self.channel)

	def on_all_raw_messages(self, c, e):
		if self.DEBUG:
			self.log(str(e.eventtype()) + " " + str(e.source()) + " " + str(e.target()) + " " + str(e.arguments()))
	
	def identify(self):
		if self.nickpassword == "":
			return
		time.sleep(1)
		self.log("Identifing myself")
		self.sendPrivateMessage("nickserv", "identify " + self.nickpassword)
		time.sleep(1)

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

	def kick(self, nick, message):
		self.connection.kick(self.channel, nick, message)


	# Adds a module to the module list
	def addModule(self, module):
		self.loadModule(module)

	# Imports the module file and adds an instance to self.modules
	def loadModule(self, module):
		mod = __import__(module)
		modobj = getattr(mod, module)() #eval("mod." + module + "()")
		modobj.setup(self.sendPrivateMessage, self.sendPublicMessage, self.sendPrivateAction, self.sendPublicAction, self.kick, self.DEBUG)
		self.activeModules.append(modobj)

    # Reload all modules
	def reload(self):
		modules = list(self.activeModules)
		self.activeModules = []
		for mod in modules:
			modtype = __import__(type(mod).__name__)
			modtype = reload(modtype)
			self.loadModule(type(mod).__name__)

	# Restarts the bot
	def restart(self):
		self.connection.disconnect("Restarting...")
		os.execl(sys.executable, sys.executable, *sys.argv)
		sys.exit(0)
		return

	# Checks modules/ for available modules (every class that is derrived from BotModule)
	def getAvailableModules(self):
		availableModules = []
		for file in os.listdir(os.path.dirname("modules/")):
			if file.endswith(".py"):
				cl = pyclbr.readmodule(file[:-3])
				for k, v in cl.items():
					name = v.name
					base = v.super
	
					if not isinstance(v.super, str):
						if not isinstance(v.super[0], str):
							base = v.super[0].name
					if "BotModule" in base:
						availableModules.append(name)
		return availableModules

	def isOper(self, nick):
		# This is weird. Bot is only present in one channel, this WILL (probably) break if he is in multiple.
		for chname, chobj in self.channels.items():
			if not chobj.is_oper(nick):
				return False
		return True

	# type: 'public', 'private'
	def parseMessage(self, c, e, type):
		nick = nm_to_n(e.source())

		if nick.lower() == "nickserv" and type == "private":
			if "This nickname is registered." in e.arguments()[0]:
				self.identify()
			return
		
		# Splitting the string into command and arguments
		args = e.arguments()[0].split()

		# Check if message is empty
		if len(args) == 0:
			return

		cmd = args[0].lower()
		args.pop(0)

		if self.DEBUG:
			self.log("Parsing " + str(type) + " command '" + str(cmd) + "' with '" + str(args) + "' from '" + str(nick) + "'")

		# Hardcoded oper commands
		if self.isOper(nick):
			if cmd == "!say":
				self.sendPublicMessage(nick, str(' '.join(args)))
				return

			if cmd == "!mod":
				if len(args) < 1:
					self.sendPrivateMessage(nick, "Usage: !mod option [module]")
					self.sendPrivateMessage(nick, "option: list, add, rm")
					return

				if args[0].lower() == "list":
					self.sendPrivateMessage(nick, "List of modules:")
					active = []
					for mod in self.activeModules:
						active.append(mod.__class__.__name__)
					
					available = self.getAvailableModules()
					for mod in available:
						status = "[ ]"
						if mod in active:
							status = "[*]"
						self.sendPrivateMessage(nick, status + " " + mod)
					return

				if args[0].lower() == "add":
					if len(args) < 2:
						self.sendPrivateMessage(nick, "Usage: !mod add module")
						return

					addmod = ""
					available = self.getAvailableModules()
					for mod in available:
						if mod.lower() == args[1].lower() or mod.lower() == args[1].lower() + "module":
							addmod = mod

					if addmod is "":
						self.sendPrivateMessage(nick, "No module added.")
						return

					try:
						self.addModule(addmod)
						self.sendPrivateMessage(nick, "Module '" + addmod + "' added.")
						self.log(nick + " added module '" + addmod + "'")
					except:
						self.sendPrivateMessage(nick, "Exception returned.")
					return

				if args[0].lower() == "rm" or args[0].lower() == "remove":
					if len(args) < 2:
						self.sendPrivateMessage(nick, "Usage: !mod rm module")
						return

					index = -1
					rmmod = args[1].lower()
					for i, mod in enumerate(self.activeModules):
						modname = mod.__class__.__name__
						if modname.lower() == rmmod or modname.lower() == rmmod + "module":
							index = i
							rmmod = modname

					if index != -1:
						del self.activeModules[index]
						self.sendPrivateMessage(nick, "Module '" + rmmod + "' removed.")
						self.log(nick + " removed module '" + rmmod + "'")
					else:		
						self.sendPrivateMessage(nick, "No module removed.")	
					return

				return

			if cmd == "!reload":
				self.log(nick + " triggered reload.")
				self.sendPrivateMessage(nick, "Reloading " + str(len(self.activeModules)) + " modules...")
				self.reload()
				self.sendPrivateMessage(nick, "done.")
				return

			if cmd == "!restart":
				self.log(nick + " triggered restart.")
				self.restart()
				return
		
		# Contact information for fsi
		if cmd == "!kontakt":
			self.sendPrivateMessage(nick, "E-Mail: kontakt@hska.info :: Tel: 0721 925-1448")
			return

		# User requested help. Send introduction string, then all help strings from all modules
		# Also, hardcoded strings.
		if cmd == "!help":
			self.sendPrivateMessage(nick, "Hallo " + nick + ", ich bin der Bot der Fachschaft Informatik. Hier sind meine Befehle:")
			self.sendPrivateMessage(nick, "!kontakt - Zeigt dir Kontaktinformationen zur Fachschaft an.")	
			for module in self.activeModules:
				module.help(nick)

			if self.isOper(nick):
				self.sendPrivateMessage(nick, "Befehle für Ops:")
				self.sendPrivateMessage(nick, "!reload - Lädt alle aktiven Module neu")
				self.sendPrivateMessage(nick, "!restart - Startet den Bot neu (nützlich nach einem Upgrade)")
				self.sendPrivateMessage(nick, "!mod - Modulverwaltung")
			return
		
		# every string that starts with an '!' is considered to be an command
		if cmd.startswith("!"):
			for module in self.activeModules:
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
		#self.log("Logged " + str(users) + " users")

	# Sends information string to webchat users coming from our site
	def inform_webusers(self, c, e):
		nick = nm_to_n(e.source())
		if nick.startswith("fsiWeb"):
			c.privmsg(nick, "Wenn du dich auf der Fachschaftsseite anmeldest, kannst du in deinen Einstellungen einen Nick für den Webchat festlegen.")
