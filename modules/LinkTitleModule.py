#! /usr/bin/env python
# coding=utf8

# Geklaut bei qchn.

from BotModule import BotModule
from urlparse import urlparse
import lxml.html


class LinkTitleModule(BotModule):
	def __init__(self):
		return

	def onMessage(self, type, args):
		if type == 'public':
			args = args.split(' ')
			for frag in args:
				o = urlparse(frag)
				if o.scheme == 'http':
					self.sendPublicMessage('Link gefunden')
					html = lxml.html.parse(frag)
					self.sendPublicMessage('[' + o.hostname + '] ' + html.find('.//title').text)

	def help(self, nick):
		return
