#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random, time

class RRouletteModule(BotModule):
	def __init__(self):
		self.size = 7
		self.lastShot = 0
		self.revolver = self.reload()
		return

	def reload(self):
		rev = []
		for n in range(0, self.size):
			rev.append('empty')

		rev[random.randint(0,self.size-1)] = 'bullet'
		
		return rev

	def command(self, nick, cmd, args, type):
		# let em shoot
		if cmd == '!roulette' and type == 'public':
			# Reload revolver if ppl havent played in a while
			if len(self.revolver) != self.size and time.time() > self.lastShot + 60*60*2:
				self.revolver = self.reload()
				self.sendPublicMessage('Neues Glück: Trommel aus ' + str(self.size) + ' Männer-Bonbon-Fächern... Ein Bonbon ist drin und tödlich.')

			if self.revolver.pop() == 'bullet':
				line = 'Bang!! ' + nick + ' geht von uns wie ein echter Mann...'
				self.kick(nick, line)
				self.revolver = self.reload()
				self.sendPublicMessage('Neues Glück: Trommel aus ' + str(self.size) + ' Männer-Bonbon-Fächern... Ein Bonbon ist drin und tödlich.')

			else:
				line = '*click* - ' + nick + ' ist ein Glückspilz. Nächster?'
			self.sendPublicMessage(line)
			self.lastShot = time.time()

		return

	def help(self, nick):
		self.sendPrivateMessage(nick, '!roulette - Russisch Roulette - zeig was in dir steckt!')
		return
