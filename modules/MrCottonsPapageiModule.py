#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random, time, re

class MrCottonsPapageiModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		return

	def onMessage(self, type, args):
		if type is not 'public':
			return

		if re.search(r'(kann|darf|hab|hät)[^\.\:\?\!]+frage', args, re.IGNORECASE):
			self.sendPublicMessage('Frag doch einfach!')

		if re.search(r'(kann|brauch|bräucht|könnt|bitte)[^\.\:\?\!]+(helf|hilf)', args, re.IGNORECASE):
			self.sendPublicMessage('Wobei?')

		if re.search(r'kennt[^\.\:\?\!]+mit', args, re.IGNORECASE):
			self.sendPublicMessage('Frag doch konkret!')

		if re.search(r'jemand[^\.\:\?\!]+(da|hier)', args, re.IGNORECASE):
			self.sendPublicMessage('Frag einfach! Die Antwort kann halt etwas dauern ...')

		if re.search(r'was[^\.\:\?\!]+sinn[^\.\:\?\!]+leben', args, re.IGNORECASE):
			self.sendPublicMessage(chr(int((math.pi * 1337) / 100)))

		probl = re.search(r'(have|has|hab|hät)[^\.\:\?\!]+(prob\w+)', args, re.IGNORECASE)
		if probl:
			# TODO
			#ans = probl.group(0)
			#es = probl.group(1)
			self.sendPublicMessage('Wasn fürn Problem?')
		return

	def help(self, nick):
		return
