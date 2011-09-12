#! /usr/bin/env python
# coding=utf8

# Add module and core folders to syspath
# TODO: Is this the right way to do this?
# see http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
import sys
sys.path.insert(0, "core/")
sys.path.insert(0, "modules/")

_DEBUG = False 

from BotCore import FSIBot

bot = FSIBot("##fsi", "fsiBot", "irc.freenode.org", 6667, _DEBUG)

#from BotModule import HelloWorldExample
#bot.addModule(HelloWorldExample())

# Add all activated modules to the bot

from BestOfModule import BestOfModule
bot.addModule(BestOfModule())

from FortuneModule import FortuneModule
bot.addModule(FortuneModule())

from MensaModule import MensaModule
bot.addModule(MensaModule())

from DeiMuddaModule import DeiMuddaModule
bot.addModule(DeiMuddaModule())

from PastebinModule import PastebinModule
bot.addModule(PastebinModule())

from BeerModule import BeerModule
bot.addModule(BeerModule())

# Start :)
bot.start()
