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
			users_tmp = self.users
			for user in users_tmp:
				if self.DEBUG:
					print "Processing " + user + "s tweets"
				try:
					statuses = self.api.GetUserTimeline(user)
				except twitter.TwitterError, err:
					if self.DEBUG:
						print 'Removing %s: %s' % (user, str(err))
					self.users.remove(user)
					pass

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
		if cmd == '!t' or cmd == '!twitter':
			if len(args) > 1 and args[0] == 'add':
				if self.DEBUG:
					print 'Adding ' + ', '.join(args[1:])
				self.users.extend(args[1:])

			elif len(args) > 1 and args[0] == 'del':
				if self.DEBUG:
					print 'Removing %s' % ', '.join(args[1:])
				for u in args[1:]:
					if u in self.users:
						self.users.remove(u)

			elif type == 'public' and 0 < len(args) < 3:
				number = 0
				if len(args) > 1:
					try:
						number = int(args[1],0)
					except:
						return
				try:
					statuses = self.api.GetUserTimeline(args[0])
				except:
					return
				if statuses is not None and 0 <= number < len(statuses):
					if self.DEBUG:
						print "Sending to channel: [" + args[0] + "] " + statuses[0].text.replace('\n','').replace('\r','')
					self.sendPublicMessage('[' + args[0] + '] ' + self.htmlparser.unescape(statuses[number].text.replace('\n','').replace('\r','')).encode('utf-8'))

	def help(self, nick):
		self.sendPrivateMessage(nick, "!t[witter] <nick>[ <i>] Zeigt den <i>-t letzten Tweet von <nick>")
		return
