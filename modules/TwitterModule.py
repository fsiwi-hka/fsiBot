#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
import twitter, time, HTMLParser

class TwitterUser:
	def __init__(self, nick):
		self.nick = nick
		self.lastUpdate = time.time()
		self.lastId = 0

	def updateTimestamp(self, timestamp):
		if timestamp > self.lastUpdate:
			self.lastUpdate = timestamp

	def updateId(self, lastId):
		if id > self.lastId:
			self.lastId = lastId

class TwitterModule(BotModule):

	def __init__(self):
		self.offset = 60 * 5
		self.users = [TwitterUser('cyberchampionka')]
		self.lastTick = time.time()
		self.api = twitter.Api()
		self.htmlparser = HTMLParser.HTMLParser()

		return

	def tick(self):
		tmp = 0
		timestamp = time.time()

		# max requests = 150!
		if timestamp - self.lastTick > self.offset:
			if self.DEBUG:
				print "Processing tick"
			users_tmp = self.users
			for user in users_tmp:
				if self.DEBUG:
					print "Processing " + user.nick + "s tweets"
				try:
					statuses = self.api.GetUserTimeline(id = user.nick, since_id = user.lastId, include_rts = True)
				except twitter.TwitterError, err:
					if str(err).startswith('Rate limit exceeded.'):
						if self.DEBUG:
							print '%s: Disabling for 60 Minutes' % str(err)
						self.lastTick = timestamp + 60*60
						return
					elif str(err).startswith('Not authorized'):
						if self.DEBUG:
							print 'Removing %s: %s' % (user.nick, str(err))
						self.users.remove(user)
					elif str(err).startswith('Not found'):
						if self.DEBUG:
							print 'Removing %s: %s' % (user.nick, str(err))
						self.users.remove(user)
					else: 
						if self.DEBUG:
							print 'Unknown Error! Removing %s: %s' % (user.nick, str(err))
						self.users.remove(user)
					continue

				except Exception as e:
					if self.DEBUG:
						print 'unhandled exception: %s' % str(e)
					continue

				tmp_created = 0
				tmp_id = 0
				for status in reversed(statuses):
					if status.created_at_in_seconds > user.lastUpdate:
						if self.DEBUG:
							print "Sending to channel: [" + user.nick + "] " + status.text.replace('\n','').replace('\r','')
						self.sendPublicMessage('[@' + self.htmlparser.unescape(user.nick).encode('utf-8') + '] ' + self.htmlparser.unescape(status.text.replace('\n','').replace('\r','')).encode('utf-8'))
						if tmp_created < status.created_at_in_seconds:
							tmp_created = status.created_at_in_seconds
						if tmp_id < status.id:
							tmp_id = status.id

				user.updateTimestamp(tmp_created)
				user.updateId(tmp_id)


			self.lastTick = timestamp

	def command(self, nick, cmd, args, type):
		if cmd == '!t' or cmd == '!twitter':
			if len(args) == 0:
				answer = "Twitter module expects at least 1 parameter!"

				if type == 'public':
					self.sendPublicMessage(answer)
				elif type == 'private':
					self.sendPrivateMessage(nick, answer)
				return

			if len(args) > 1 and args[0] == 'add':
				if self.DEBUG:
					print 'Adding ' + ', '.join(args[1:])
				self.users.extend([TwitterUser(u) for u in args[1:]])

			elif len(args) > 1 and args[0] == 'del':
				if self.DEBUG:
					print 'Removing %s' % ', '.join(args[1:])
				for u in args[1:]:
					for user in self.users:
						if user.nick == u:
							self.users.remove(user)

			elif args[0] == 'list':
				if self.DEBUG:
					print 'Printing userlist ' + ', '.join(user.nick for user in self.users)

				answer = '[Twitter] ' + ', '.join(user.nick for user in self.users)

				if type == 'public':
					self.sendPublicMessage(answer)
				elif type == 'private':
					self.sendPrivateMessage(nick, answer)

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
					self.sendPublicMessage('[@' + args[0] + '] ' + self.htmlparser.unescape(statuses[number].text.replace('\n','').replace('\r','')).encode('utf-8'))

	def help(self, nick):
		self.sendPrivateMessage(nick, "!t[witter] <nick>[ <i>] Zeigt den <i>-t letzten Tweet von <nick>")
		self.sendPrivateMessage(nick, "!t[witter] add <nick>[ <nick2>][ <nick3>]... Fügt <nick> hinzu")
		self.sendPrivateMessage(nick, "!t[witter] del <nick>[ <nick2>][ <nick3>]... Entfernt <nick>")
		self.sendPrivateMessage(nick, "!t[witter] list Zeigt die derzeit gefollowten User an")
		
		return
