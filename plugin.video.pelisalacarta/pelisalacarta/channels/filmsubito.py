# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.keys import Keys
from lxml import etree
from io import StringIO
import urlparse, urllib2, urllib, re, xbmcplugin, xbmcgui, xbmcaddon, xbmc
import os, sys, time

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import json


__channel__ = "filmsubito"
__category__ = "F"
__type__ = "generic"
__title__ = "filmsubito"
__language__ = "IT"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.filmsubito  mainlist")

    itemlist = []
    itemlist.append(
        Item(channel=__channel__, action="peliculas", title="Serie TV", url="http://filmsubito.tv/film-streaming.html"))
    itemlist.append(Item(channel=__channel__, action="peliculas", title="Serie TV Anni 80",
                         url="http://filmsubito.tv/film-streaming.html"))
    itemlist.append(Item(channel=__channel__, action="peliculas", title="Cartoni Animati anni 80",
                         url="http://filmsubito.tv/film-streaming.html"))
    itemlist.append(Item(channel=__channel__, action="peliculas", title="Documentari",
                         url="http://filmsubito.tv/film-streaming.html"))

    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.filmsubito peliculas")
    itemlist = []
    print "fu"