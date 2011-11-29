#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
from time import *
import os, sys, random
from collections import defaultdict
import random, pickle, os

class MarkovChatter(BotModule):
	def __init__(self):
		self.markov = defaultdict(list)
		self.delimiter = "\n"
		
		if os.path.exists("chatter.db"):
			self.markov = pickle.load(open("chatter.db", "rb"))

	def addToBrain(self, msg, length):
		buf = [self.delimiter] * length
		for word in msg.split():
			self.markov[tuple(buf)].append(word)
			del buf[0]
			buf.append(word)
		self.markov[tuple(buf)].append(self.delimiter)
		pickle.dump(self.markov, open("chatter.db", "wa+b"), -1)

	def buildSentence(self, msg, length, max=150):
		buf = msg.split()[:length]
		if len(msg.split()) > length:
			message = buf[:]
		else:
			message = []
			for i in xrange(length):
				message.append(random.choice(self.markov[random.choice(self.markov.keys())]))
		for i in xrange(max):
			try:
				next_word = random.choice(self.markov[tuple(buf)])
			except IndexError:
				continue
			if next_word == self.delimiter:
				break
			message.append(next_word)
			del buf[0]
			buf.append(next_word)
		return ' '.join(message)

class MarkovModule(BotModule):
	def __init__(self):
		self.markov = MarkovChatter()
		return

	def command(self, nick, cmd, args, type):
		return

	def onMessage(self, type, msg):
		if type == 'public':
			if(msg.startswith(self.nick + ":")):
				self.sendPublicMessage(self.markov.buildSentence(msg[7:], 2))
			else:
				self.markov.addToBrain(msg, 2)
		

	def help(self, nick):
		return
