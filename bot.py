#! /usr/bin/env python
# coding=utf8

# Add module and core folders to syspath
# TODO: Is this the right way to do this?
# see http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
import sys, os
sys.path.insert(0, "core/")
sys.path.insert(0, "modules/")
sys.path.insert(0, "modules/config/")

_DEBUG = False 

from BotCore import FSIBot

bot = FSIBot("##fsi", "fsiBot", "irc.freenode.org", 6667, _DEBUG)

# Add activated modules to the bot

bot.addModule("BestOfModule")
bot.addModule("FortuneModule")
bot.addModule("MensaModule")
bot.addModule("DeiMuddaModule")
bot.addModule("PastebinModule")
bot.addModule("BeerModule")
bot.addModule("RRouletteModule")

# Start :)
bot.start()
