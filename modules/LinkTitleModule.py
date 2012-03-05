#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule
from urlparse import urlparse
import lxml.html
import re


class LinkTitleModule(BotModule):
	def __init__(self):
		return

	def onMessage(self, type, args):
		if type == 'public':
			args = args.split(' ')
			for frag in args:
				o = urlparse(frag)
				if o.scheme == 'http':
#					try:
						html = lxml.html.parse(frag)
						answer = re.sub(r'\s+', ' ', '[' + o.hostname + '] ' + html.find('.//title').text)
						self.sendPublicMessage(answer)						
#self.sendPublicMessage('[' + o.hostname + '] ' + re.sub('\s{2,}', ' ', html.find('.//title').text.replace('\n','').replace('\r', '')))
#					except:
#						pass

	def command(self, nick, cmd, args, type):
		return
	def help(self, nick):
		return
