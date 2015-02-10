#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random, time, re

class MrCottonsPapageiModule(BotModule):
	def __init__(self):
		return

	def command(self, nick, cmd, args, type):
		if type not 'public':
			return

		if re.match(r'(?i)kann|dar|hab|hät)[^\.\:\?\!]+frage', cmd):
			self.sendPublicMessage('Frag doch einfach!')



#		if cmd == '!roulette' and type == 'public':
#			# Reload revolver if ppl havent played in a while
#			if len(self.revolver) != self.size and time.time() > self.lastShot + 60*60*2:
#				self.revolver = self.reload()
#				self.sendPublicMessage('Neues Glück: Trommel aus ' + str(self.size) + ' Männer-Bonbon-Fächern... Ein Bonbon ist drin und tödlich.')
#
#			if self.revolver.pop() == 'bullet':
#				line = 'Bang!! ' + nick + ' geht von uns wie ein echter Mann...'
#				self.sendPublicMessage(line)
#				self.kick(nick, line)
#				self.revolver = self.reload()
#				self.sendPublicMessage('Neues Glück: Trommel aus ' + str(self.size) + ' Männer-Bonbon-Fächern... Ein Bonbon ist drin und tödlich.')
#
#			else:
#				self.sendPublicMessage('*click* - ' + nick + ' ist ein Glückspilz. Nächster?')
#			self.lastShot = time.time()

		return

	def help(self, nick):
		self.sendPrivateMessage(nick, '!roulette - Russisch Roulette - zeig was in dir steckt!')
		return
