# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
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
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.filmsubito  mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Serie TV" , url="http://filmsubito.tv" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Serie TV Anni 80" , url="http://filmsubito.tv" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Cartoni Animati anni 80" , url="http://filmsubito.tv" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Documentari" , url="http://filmsubito.tv" ))

    return itemlist


def peliculas (item):
    logger.info("pelisalacarta.filmsubito peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    patron  = '<div class="item">\s*'
    patron += '<a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?'
    patron += '<div class="img">\s*'
    patron += '<img.*?src="([^>"]+)'

    matches = re.compile(patron,re.DOTALL).findall(data)
    #print item.url
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="grabing", title=title , url=url , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )