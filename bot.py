#! /usr/bin/env python
# coding=utf8

# Add module and core folders to syspath
# TODO: Is this the right way to do this?
# see http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
import sys, os, config
sys.path.insert(0, "thirdparty/")
sys.path.insert(0, "core/")
sys.path.insert(0, "modules/")
sys.path.insert(0, "modules/config/")

from BotCore import FSIBot

# Open config file
cfg = config.Config(file("bot.config"))
botcfg = cfg.bot

bot = FSIBot(botcfg.channel, botcfg.name, botcfg.server, botcfg.port, botcfg.debug)

# Add activated modules to the bot
for mod in botcfg.modules:
    bot.addModule(mod)

# Start :)
bot.start()
