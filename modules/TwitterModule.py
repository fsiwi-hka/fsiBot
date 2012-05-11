#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
import twitter, time, HTMLParser

class TwitterModule(BotModule):

	def __init__(self):
		self.offset = 30
		self.users = ['cyberchampionka']
		self.lastTick = time.time()
		self.api = twitter.Api()
		self.lastUpdate = 0
		self.htmlparser = HTMLParser.HTMLParser()

		for user in self.users:
			statuses = self.api.GetUserTimeline(user)
			for status in statuses:
				if status.created_at_in_seconds > self.lastUpdate:
					self.lastUpdate = status.created_at_in_seconds

		return
	def tick(self):
		tmp = 0
		timestamp = time.time()
		if timestamp - self.lastTick > self.offset:
#			print "Processing tick"
			for user in self.users:
#				print "Processing " + user + "s tweets"
				statuses = self.api.GetUserTimeline(user)
				for status in statuses:
					if status.created_at_in_seconds > self.lastUpdate:
#						print "Sending to channel: [" + user + "] " + status.text.replace('\n','').replace('\r','')
						self.sendPublicMessage('[' + self.htmlparser.unescape(user).encode('utf-8') + '] ' + self.htmlparser.unescape(status.text).encode('utf-8'))

						if status.created_at_in_seconds > tmp:
							tmp = status.created_at_in_seconds

			self.lastTick = timestamp
			if tmp > self.lastUpdate:
				self.lastUpdate = tmp

	def command(self, nick, cmd, args, type):
		return

	def help(self, nick):
		#self.sendPrivateMessage(nick, "")
		return
