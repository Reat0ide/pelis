# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from bs4 import BeautifulSoup
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import os, sys
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "guardarefilm"
__category__ = "F"
__type__ = "generic"
__title__ = "guardarefilm"
__language__ = "IT"

DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.guardarefilm  mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Lista Serie TV" , url="http://www.guardarefilm.net/serie-tv-streaming/" ))
    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.itastreaming_test peliculas")
    itemlist = []
    root_url='http://www.guardarefilm.net'
    data = scrapertools.cache_page(item.url)

    #extract url and thumb_url
    patron  = '<div class="poster">'
    patron += '<a href="?([^>"]+)"?.*?<img.*?src="([^>"]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)

    #scrapertools.printMatches(matches)

    pattern = '<div class="label"><a href="(.*?)"(.*?)</a>'
    matches_2 = re.compile(pattern,re.DOTALL).findall(data)


    for i in range(len(matches)):
        url = matches[i][0]
        thumbnail_url = root_url + matches[i][1]
        title = matches_2[i][1]
        title = title[1:]
        itemlist.append( Item(channel=__channel__, action="season", title=title, url=url , thumbnail=thumbnail_url , folder=True) )

    return itemlist

#grab all the episodes
def season(item):
    logger.info("pelisalacarta.guardarefilm season")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    print item.url
    #create seasons menu
    pattern = '<div class="tab-pane fade" id="([^>"]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for result in matches:
        itemlist.append( Item(channel=__channel__, action="grabing", url=item.url, title=result, folder=True) )

    return itemlist


def grabing(item):
    itemlist = []
    data = scrapertools.cache_page(item.url)
    print item.url
    print item.title

    pattern = '<div class="tab-pane fade" id="' + item.title + '">\s*'
    pattern += '<ul class="reset series_list">\s*'
    pattern += '<li id="([^>"]+).*?<a href="#" class="links-sd".*?data-link="(.*?)"'
    matches = re.compile(pattern,re.MULTILINE).findall(data)
    print matches

    #test with bs4
    soup = BeautifulSoup(data)
    for div in soup.find_all('div', attrs={'id' : item.title}):
        print div
        for li in div.find_all('data-link'):
            print li



def playit(item):

    itemlist = []
    print "bar"
    return itemlist
