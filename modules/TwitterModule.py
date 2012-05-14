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
			try:
				statuses = self.api.GetUserTimeline(user)
		
				for status in statuses:
					if status.created_at_in_seconds > self.lastUpdate:
						self.lastUpdate = status.created_at_in_seconds
			except:
				pass

		return
	def tick(self):
		tmp = 0
		timestamp = time.time()
		if timestamp - self.lastTick > self.offset:
			if self.DEBUG:
				print "Processing tick"
			for user in self.users:
				if self.DEBUG:
					print "Processing " + user + "s tweets"
				try:
					statuses = self.api.GetUserTimeline(user)
				except:
					return
				for status in statuses:
					if status.created_at_in_seconds > self.lastUpdate:
						if self.DEBUG:
							print "Sending to channel: [" + user + "] " + status.text.replace('\n','').replace('\r','')
						self.sendPublicMessage('[' + self.htmlparser.unescape(user).encode('utf-8') + '] ' + self.htmlparser.unescape(status.text.replace('\n','').replace('\r','')).encode('utf-8'))

						if status.created_at_in_seconds > tmp:
							tmp = status.created_at_in_seconds

			self.lastTick = timestamp
			if tmp > self.lastUpdate:
				self.lastUpdate = tmp

	def command(self, nick, cmd, args, type):
		if type == 'public' and (cmd == '!t' or cmd == '!twitter') and 0 < len(args) < 3:
			number = 0
			if len(args) > 1:
				try:
					number = int(args[1],0)
				except:
					return
			statuses = self.api.GetUserTimeline(args[0])
			if statuses is not None and 0 <= number < len(statuses):
				if self.DEBUG:
					print "Sending to channel: [" + args[0] + "] " + statuses[0].text.replace('\n','').replace('\r','')
				self.sendPublicMessage('[' + args[0] + '] ' + self.htmlparser.unescape(statuses[number].text.replace('\n','').replace('\r','')).encode('utf-8'))

	def help(self, nick):
		self.sendPrivateMessage(nick, "!t[witter] <nick>[ <i>] Zeigt den <i>-t letzten Tweet von <nick>")
		return
