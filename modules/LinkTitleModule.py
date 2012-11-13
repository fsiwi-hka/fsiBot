#! /usr/bin/env python
# coding=utf8

# TODO:
# Forenlinks nicht auflösen, da Threadtitel nicht gelesen werden können
#

from BotModule import BotModule
from urlparse import urlparse
import urllib2, lxml.html, re, HTMLParser

class LinkTitleModule(BotModule):
	maxredirects = 10

	def __init__(self):
		self.htmlparser = HTMLParser.HTMLParser()
		return

	def onMessage(self, type, args):
		if type == 'public':
			args = args.split(' ')
			for frag in args:
				o = urlparse(frag)
				if o.scheme == 'http' or o.scheme == 'https':
					uri = frag

					if self.DEBUG:
						print('parsing url "' + uri + '"\n')
				
					try:
						if self.DEBUG:
							print(uri + ": fetching ...")
						headers = {
							'Accept': 'text/html',
							'User-Agent': 'Mozilla/5.0 (fsiBot)',
							'Referrer': 'http://www.hska.info'
							}
						req = urllib2.Request(uri, headers = headers)
						u = urllib2.urlopen(req, timeout=10)
						info = u.info()
						newUrl = u.geturl()
#						u.close

						i = urlparse(newUrl)

						if i.hostname == 'localhost' or i.hostname.startswith('127.'):
							if self.DEBUG:
								print (newUrl + ' matched for localhost')
							return

						try:
							mtype = info['content-type']
							if self.DEBUG:
								print(newUrl + ": Content-Type is " + mtype)
						except:
							if self.DEBUG:
								print(newUrl + ": Could not get the Content-Type")
							return

						if not (('/html' in mtype) or ('/xhtml' in mtype)):
							if self.DEBUG:
								print(newUrl + ": Document is not HTML")
							return


						if self.DEBUG:
							print(newUrl + ": opening ...")
#						req = urllib2.Request(newUrl, headers = headers)
#						u = urllib2.urlopen(req)
						bytes = u.read(4096)
						if self.DEBUG:
							print("read: " + bytes)
						u.close

					except IOError as e:
						if self.DEBUG:
							print(uri + ": Can't connect to: " + str(e))
						return

					r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
					m = r_title.search(bytes)

					if m:
						title = m.group(1)
						if self.DEBUG:
							print("parsed html, title is: " + title)

						try:
							title = self.htmlparser.unescape(title.decode('utf-8')).encode('utf-8')
							if self.DEBUG:
								print("unescaped title to: " + title)
								
						except Exception as e:
							if self.DEBUG:
								print("decoding title crashed with: %s" % str(e))

						if (len(title) > 200):
							title = title[:200] + "[...]"

						if title:
							try: title.decode('utf-8')
							except:
								try: title = title.decode('iso-8859-1').encode('utf-8')
								except: title = title.decode('cp1252').encode('utf-8')
							else: pass
						else:
							if self.DEBUG:
								print(newUrl + ": Title is empty")

						answer = re.sub(r'\s+', ' ', '[' + i.hostname + '] ' + title)
						self.sendPublicMessage(answer)
					else:
						if self.DEBUG:
							print(newUrl + ": No title found")


	def command(self, nick, cmd, args, type):
		return
	def help(self, nick):
		return
