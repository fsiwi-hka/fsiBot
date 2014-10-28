#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

class AliasModule(BotModule):

	# define all alias helpers here
	aliases = {
		'!intra': '!link intra'
	}

	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		# check if the alias exists
		if cmd in aliases:
			self.sendPublicMessage(aliases[cmd]) # if it exists post the matching alias

	def help(self, nick):
		self.sendPrivateMessage(nick, "Alias module")
		return
