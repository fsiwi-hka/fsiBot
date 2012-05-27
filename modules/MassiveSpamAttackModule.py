#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random

class MassiveSpamAttackModule(BotModule):
	def _init_(self):
		return

	def command(self, nick, cmd, args, type):

		if cmd == "!msa":
			msg = ""
			
			if len(args) != 0:
				mode = args[0]
				users = self.getAllUsers(nick, mode)

				if len(users) != 0:
					for user in users:
						if len(msg) != 0:
							msg += ", "
						msg += user

					msg += ": "
					for chunk in args[1::1]:
						msg += chunk + " "

					self.sendPublicMessage("Von " + nick + " an " + msg)



	def help(self, nick):
		self.sendPrivateMessage(nick, "!msa arg message - arg: all, fs. MassiveSpamAttak nur für Ops. ")
		return