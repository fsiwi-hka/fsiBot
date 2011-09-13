#! /usr/bin/env python
# coding=utf8

from BotModule import BotModule

import os, sys, random

class RRouletteModule(BotModule):
    def __init__(self):
        self.size = 7
        self.revolver = self.reload()
        return

    def reload(self):
        rev = []
        for n in range(0, self.size):
            rev.append('empty')

        rev[random.randint(0,self.size-1)] = 'bullet'

        return rev



    def command(self, nick, cmd, args, type):
        #let em shoot
        if cmd == '!roulette' and type != 'private':
            if self.revolver.pop() == 'bullet':
                line = 'Bang!! ' + nick + ' geht von uns wie ein echter Mann... Neues Glück: Trommel aus ' + str(self.size) + ' Männer-Bonbon-Fächern... Ein Bonbon ist drin und tödlich.'
                self.revolver = self.reload()
            else:
                line = '*click* - ' + nick + ' ist ein Glückspilz. Nächster?'
            self.sendPublicMessage(line)

        return

    def help(self, nick):
        self.sendPrivateMessage(nick, '!roulette - Russisch Roulette - zeig was in dir steckt!')
        return

# vim: set ts=8 sw=4 tw=0 :
