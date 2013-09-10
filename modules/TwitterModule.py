#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
import twitter, time, HTMLParser, config

class TwitterModule(BotModule):

	def __init__(self):
		self.cfg = config.Config(file("bot.config")).twitter
		self.htmlparser = HTMLParser.HTMLParser()
		self.api = twitter.Api(consumer_key=self.cfg.consumer_key,
								consumer_secret=self.cfg.consumer_secret,
								access_token_key=self.cfg.access_token_key,
								access_token_secret=self.cfg.access_token_secret)

		self.authorized = False

		if self.api.VerifyCredentials() is not None:
			self.authorized = True
			self.refreshFriendlist()
			self.last_id = self.api.GetHomeTimeline()[0].id

		self.last_tick = 0

		return

	def tick(self):
		cur_time = time.time()

		offset = self.cfg.update_interval*60

		if cur_time - self.last_tick < offset:
			return

		if self.cfg.DEBUG:
			print "Processing tick"

		if self.authorized is True:
			try:
				timeline = self.api.GetHomeTimeline(since_id=self.last_id, include_entities=False, exclude_replies=True)
			except twitter.TwitterError as err:
				if str(err).startswith("[{u'message': u'Rate limit exceeded"):
					if self.cfg.DEBUG:
						print '%s: Disabling for 5 Minutes' % str(err)

					self.last_tick = cur_time + 60*5
					return
				else: 
					if self.cfg.DEBUG:
						print 'Unknown Error: %s' % str(err)

					# for debuging ...
					self.last_tick = cur_time + 60*15
					return

			except Exception as e:
				if self.cfg.DEBUG:
					print 'unhandled exception: %s' % str(e)
				return			

			if len(timeline) > 0:
				for status in reversed(timeline):

					if status.GetId() > self.last_id:
						self.last_id = status.GetId()

					if status.GetRetweeted_status() is not None:
						if self.cfg.DEBUG:
							print 'Replacing retweet with original tweet'
						status = status.GetRetweeted_status()

					if self.cfg.DEBUG:
						print "Sending to channel: [" + status.GetUser().GetScreenName() + "] " + status.GetText().replace('\n','').replace('\r','')
					self.answer('public', '', '[@' + self.htmlparser.unescape(status.GetUser().GetScreenName()).encode('utf-8') + '] ' + self.htmlparser.unescape(status.GetText().replace('\n','').replace('\r','')).encode('utf-8'))				

		if self.cfg.DEBUG:
			try:
				api_limit_status = self.api.GetRateLimitStatus()
				print "Remaining API requests: %d" % api_limit_status['resources']['application']['/application/rate_limit_status']['remaining']
			except:
				pass

		self.last_tick = cur_time


	def command(self, nick, cmd, args, type):
		if cmd == '!t' or cmd == '!twitter':
			if len(args) == 0:
				self.answer(type, nick, "TwitterModule expects at least 1 parameter!")
				return

			if self.isOper(nick) and self.authorized is True and args[0] == 'add' and len(args) > 1:
				if self.cfg.DEBUG:
					print 'Adding ' + ', '.join(args[1:])

				for nick in args[1:]:
					try:
						res = self.api.CreateFriendship(screen_name=nick)
					except:
						return

					if res is not None:
						if self.cfg.DEBUG:
							print 'Added %s' % nick
					else:
						if self.cfg.DEBUG:
							print 'Failure adding %s' % nick

				self.refreshFriendlist()
				return

			if self.isOper(nick) and self.authorized is True and args[0] == 'del' and len(args) > 1:
				if self.cfg.DEBUG:
					print 'Removing %s' % ', '.join(args[1:])

				for nick in args[1:]:
					try:
						res = self.api.DestroyFriendship(screen_name=nick)
					except:
						return

					if res is not None:
						if self.cfg.DEBUG:
							print 'Removed %s' % nick
					else:
						if self.cfg.DEBUG:
							print 'Failure removing %s' % nick									

				self.refreshFriendlist()
				return

			if self.isOper(nick) and self.authorized is True and args[0] == 'refresh':
				if self.cfg.DEBUG:
					print 'Refreshing friendslist'

				self.refreshFriendlist()
				return

			if self.authorized is True and args[0] == 'list':
				if self.cfg.DEBUG:
					print 'Printing userlist ' + ', '.join(user.GetScreenName() for user in self.friends)

				self.answer(type, nick, '[Twitter] ' + ', '.join(user.GetScreenName() for user in self.friends))
				return

			if 1 <= len(args) < 3:
				index = 0
				if len(args) > 1:
					try:
						index = int(args[1],0)
					except:
						return

				try:
					user_timeline = self.api.GetUserTimeline(screen_name=args[0])
				except:
					return

				if user_timeline is not None and 0 <= index < len(user_timeline):
					if self.cfg.DEBUG:
						print "User Tweet: [" + args[0] + "] " + user_timeline[index].GetText().replace('\n','').replace('\r','')
					self.answer(type, nick, '[@' + args[0] + '] ' + self.htmlparser.unescape(user_timeline[index].GetText().replace('\n','').replace('\r','')).encode('utf-8'))					

				return

	def help(self, nick):
		self.answer('private', nick, "!t[witter] <nick>[ <i>] - Zeigt den <i>-t letzten Tweet von <nick>")
		self.answer('private', nick, "!t[witter] list - Zeigt die derzeit gefollowten User an")

		if self.isOper(nick):
			self.answer('private', nick, "!t[witter] add <nick>[ <nick2>][ <nick3>]... - Fügt <nick> hinzu")
			self.answer('private', nick, "!t[witter] del <nick>[ <nick2>][ <nick3>]... - Entfernt <nick>")
			self.answer('private', nick, "!t[witter] refresh - Lädt die Friendlist neu")

	def answer(self, type, nick, message):
		if type == 'public':
			self.sendPublicMessage(message)
		elif type == 'private':
			self.sendPrivateMessage(nick, message)
		elif self.cfg.DEBUG:
			print "Unknown message type: %s" % type

	def refreshFriendlist(self):
		self.friends = self.api.GetFriends()
