#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import feedparser
import sqlite3
import time
import datetime
import HTMLParser
from lxml import etree

import htmlentitydefs
class HTMLTextExtractor(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

class BBFeed(object):
    DATABASE_FILE = 'bb_database.sqlite'
    def __init__(self, name):
        self.url = 'http://www.iwi.hs-karlsruhe.de/Intranetaccess/REST/rssfeed/newsbulletinboard/' + str(name)
        self.name = name
        self.database = BBFeed.DATABASE_FILE
        self.connection = sqlite3.connect(self.database)
        self._initDatabase()

    def _initDatabase(self):
        self.connection.execute('CREATE TABLE IF NOT EXISTS ' + str(self.name) + ' (`title`, `author`, `published`, `content`, `posted`)')
        return

    def parse(self):
        data = feedparser.parse(self.url)
        cursor = self.connection.cursor()

        htmlparser = HTMLParser.HTMLParser()
        for entry in data.entries:
            dt = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
            unixtime = str(int(dt.strftime("%s")))

            if len(entry.content) != 1:
                continue
            
            cdata = htmlparser.unescape(entry.content[0].value)
            # RSS Feed cdata is not valid, '>' is missing...
            doc = etree.fromstring('<s>' + cdata + '></s>')
            content = html_to_text(doc.text)

            cursor.execute('SELECT * FROM ' + str(self.name) + ' WHERE title=? AND published=?', (entry.title, unixtime))

            # Check for duplicate
            if cursor.fetchall():
                continue

            cursor.execute('INSERT INTO ' + str(self.name) + '(`title`, `author`, `published`, `content`, `posted`) VALUES (?, ?, ?, ?, 0)',
                           (entry.title, entry.author, unixtime, content))
        self.connection.commit()

    def posted(self, id):
        cursor = self.connection.cursor()
        cursor.execute('UPDATE ' + str(self.name) + ' SET posted=1 WHERE rowid=?', (str(id)))

    def getEntries(self, time=0):
        cursor = self.connection.cursor()
        cursor.execute('SELECT `rowid`, `title`, `author`, `published`, `content`, `posted` FROM ' + str(self.name))
        entries = []
        for entry in cursor.fetchall():
            d = datetime.datetime.fromtimestamp(int(entry[3])).strftime('%d.%m. %H:%M')

            posted = False
            if int(entry[5]) != 0:
                posted = True

            e = {'id': entry[0], 'title': entry[1].encode('utf8'), 'author': entry[2].encode('utf8'), 
                 'published': d, 'content': entry[4].encode('utf8'), 'posted': posted}

            if int(entry[3]) > time:
                entries.append(e)

        return entries

class BulletinBoardModule(BotModule):
    def __init__(self):
        self.last_tick = time.time() - 60*60*24
        self.parsers = [BBFeed('INFB'), BBFeed('INFM'), BBFeed('MKIB')]

    def tick(self):
        cur_time = time.time()
        offset = 5*60

        if cur_time - self.last_tick < offset:
            return
        self.last_tick = cur_time

        for parser in self.parsers:
            parser.parse()
            entries = parser.getEntries(cur_time - offset - 1)
            for entry in entries:
                if entry['posted'] == False:
                    self.sendPublicMessage(parser.name + ' ' + entry['published'] + ': ' + entry['content'])
                    parser.posted(entry['id'])

    def command(self, nick, cmd, args, type):
        if cmd == "!bb" and len(args) == 1:
            entries = []
            for parser in self.parsers:
                print str.lower(parser.name)
                if str.lower(parser.name) == str.lower(args[0]):
                    entries = parser.getEntries()
            for entry in entries:
                self.answer('private', nick, entry['published'] + ': ' + entry['content'])

    def help(self, nick):
        self.answer('private', nick, "!bb <studiengang> - Zeigt letze Bulletin-Board Eintraege aus dem Studiengang an")
        self.answer('private', nick, "Studiengang: INFB, INFM, MKIB")

    def answer(self, type, nick, message):
        if type == 'public':
            self.sendPublicMessage(message)
        elif type == 'private':
            self.sendPrivateMessage(nick, message)