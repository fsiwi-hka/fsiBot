#! /usr/bin/env python
# coding=utf8

#Teile des Codes:
#Copyright 2008, Sean B. Palmer, inamidst.com
#Licensed under the Eiffel Forum License 2.
#http://inamidst.com/phenny/
	

from BotModule import BotModule
from urlparse import urlparse
import urllib2
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
				if o.scheme == 'http' or o.scheme == 'https':
					uri = frag
					if self.DEBUG:
						print('parsing url "' + uri + '"\n')
				
					localhost = [
						'http://localhost/', 'http://localhost:80/',
						'http://localhost:8080/', 'http://127.0.0.1/',
						'http://127.0.0.1:80/', 'http://127.0.0.1:8080/',
						'https://localhost/', 'https://localhost:80/',
						'https://localhost:8080/', 'https://127.0.0.1/',
						'https://127.0.0.1:80/', 'https://127.0.0.1:8080/',
					]

					for s in localhost:
						if uri.startswith(s):
							if self.DEBUG:
								print(uri + ": acces for localhost denied")
							return

					try:
						redirects = 0
						while True:
							if self.DEBUG:
								print(uri + ": fetching ...")
							headers = {
								'Accept': 'text/html',
								'User-Agent': 'Mozilla/5.0 (fsiBot)'
								}
							req = urllib2.Request(uri, headers = headers)
							u = urllib2.urlopen(req)
							info = u.info()
							u.close()

							if not isinstance(info, list):
								status = '200'
							else:
								status = str(info[1])
								info = info[0]
							if status.startswith('3'):
								uri = urlparse.urljoin(uri, info['Location'])
							else:
								break

							redirects += 1
							if redirects >= 10:
								if self.DEBUG:
									print(url + ": To many redirects")
								return

						try:
							mtype = info['content-type']
						except:
							if self.DEBUG:
								print(url + ": Couldnt get the Content-Type")
							return

						if not (('/html' in mtype) or ('/xhtml' in mtype)):
							if self.DEBUG:
								print(url + ": Document isnt HTML")
							return


						if self.DEBUG:
							print(uri + ": opening ...")
						u = urllib2.urlopen(req)
						bytes = u.read(262144)
						if self.DEBUG:
							print("read: " + bytes)
						u.close

					except IOError:
						if self.DEBUG:
							print(url + ": Can't connet to")
						return

					r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
					m = r_title.search(bytes)

					if m:
						title = m.group(1)
						if self.DEBUG:
							print("parsed html, title is: " + title)

						if (len(title) > 200):
							title = title[:200] + "[...]"

						def e(m):
							entity = m.group(0)
							if entity.startswith('&#x'):
								cp = int(entity[3:-1], 16)
								return unichr(cp).encode('utf-8')
							elif entity.startswith('&#'):
								cp = int(entity[2:-1])
								return unichr(cp).encode('utf-8')
							else:
								char = name2codepoint[entity[1:-1]]
								return unichr(char).encode('utf-8')
						r_entity = re.compile(r'&[A-Za-z0-9#]+;')
						title = r_entity.sub(e, title)

						if title:
							try: title.decode('utf-8')
							except:
								try: title = title.decode('iso-8859-1').encode('utf-8')
								except: title = title.decode('cp1252').encode('utf-8')
							else: pass
						else: title = '[Title is empty.]'

						answer = re.sub(r'\s+', ' ', '[' + o.hostname + '] ' + title)
						self.sendPublicMessage(answer)
					else:
						if self.DEBUG:
							print(url + ": Title is empty")
				else:
					if self.DEBUG:
						print(url + ": No title found")


	def command(self, nick, cmd, args, type):
		return
	def help(self, nick):
		return
