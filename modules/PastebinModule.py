#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
from PastebinModuleConfig import PastebinModuleConfig

import os, sys, random, commands, MySQLdb

class PastebinModule(BotModule):
	def __init__(self):
		self.password = PastebinModuleConfig().getPassword()
		return

	def command(self, nick, cmd, args, type):
		if cmd == "!paste" or cmd == "!p" :
			if len(args) == 0:
				output = "https://paste.hska.info"
			else:
				conn = MySQLdb.connect(	host = "localhost",
										user = "pastebin",
										passwd = self.password,
										db = "pastebin")
				cursor = conn.cursor()
				foo = ' '.join(args)
				cursor.execute('SELECT pid FROM pastes WHERE name = %s ORDER BY created DESC LIMIT 1', (foo))
				row = cursor.fetchone()
				if row is not None:
					output = "https://paste.hska.info/view/" + row[0]
				else:
					output = "Kein Paste von " + foo + " gefunden."
				cursor.close()
				conn.close()
			if type == "private":
				self.sendPrivateMessage(nick, output)
			else:
				self.sendPublicMessage(output)

	def help(self, nick):
		self.sendPrivateMessage(nick, "!paste [name] - Link zum letzten Post des angegeben Users oder zum Pastebin.")
		return
