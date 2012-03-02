#! /usr/bin/env python
# coding=utf8

# Geklaut bei qchn.

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
					try:
						html = lxml.html.parse(frag)
						self.sendPublicMessage('[' + o.hostname + '] ' + re.sub('\s{2,}', ' ', html.find('.//title').text.replace('\n','')))
					except:
						pass

	def command(self, nick, cmd, args, type):
		return
	def help(self, nick):
		return
