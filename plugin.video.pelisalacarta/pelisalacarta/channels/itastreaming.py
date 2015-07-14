# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# created by Reat0ide 2015 for pelisalacarta
#------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import os, sys, time

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import json
   

__channel__ = "itastreaming"
__category__ = "F"
__type__ = "generic"
__title__ = "itastreaming"
__language__ = "IT"

DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.itastreaming  mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="ultimi film inseriti..." , url="http://itastreaming.tv" ))
    itemlist.append( Item(channel=__channel__ , action="search", title="Cerca Film"))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="animazione" , url="http://itastreaming.tv/genere/animazione" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="avventura" , url="http://itastreaming.tv/genere/avventura" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="azione" , url="http://itastreaming.tv/genere/azione" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="biografico" , url="http://itastreaming.tv/genere/biografico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="comico" , url="http://itastreaming.tv/genere/comico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="commedia" , url="http://itastreaming.tv/genere/commedia" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="documentario" , url="http://itastreaming.tv/genere/documentario" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="drammatico" , url="http://itastreaming.tv/genere/drammatico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="erotico" , url="http://itastreaming.tv/genere/erotico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="fantascienza" , url="http://itastreaming.tv/genere/fantascienza" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="fantasy" , url="http://itastreaming.tv/genere/fantasy" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="gangstar" , url="http://itastreaming.tv/genere/gangstar" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="giallo" , url="http://itastreaming.tv/genere/giallo" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="guerra" , url="http://itastreaming.tv/genere/guerra" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="horror" , url="http://itastreaming.tv/genere/horror" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="musical" , url="http://itastreaming.tv/genere/musical" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="romantico" , url="http://itastreaming.tv/genere/romantico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="storico" , url="http://itastreaming.tv/genere/storico" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="thriller" , url="http://itastreaming.tv/genere/thriller" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="western" , url="http://itastreaming.tv/genere/western" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD" , url="http://itastreaming.tv/qualita/hd" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="DVD-RIP" , url="http://itastreaming.tv/qualita/dvdripac3" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="CAM" , url="http://itastreaming.tv/qualita/cam" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD-MD" , url="http://itastreaming.tv/qualita/hd-md" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="HD-TS" , url="http://itastreaming.tv/qualita/hd-ts" ))
         
    return itemlist

#searching for films
def search(item, text):
    logger.info("[itastreaming.py] search " + text)
    itemlist = []
    text = text.replace(" ", "%20")
    item.url = "http://itastreaming.tv/?s=" + text
    try:

        data = scrapertools.cache_page(item.url)
        pattern = '<img class="imx" style="margin-top:0px;" src="?([^>"]+)"?.*?alt="?([^>"]+)"?.*?'
        pattern += '<h3><a href="?([^>"]+)"?.*?</h3>'
        matches = re.compile(pattern,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for scrapedthumbnail, scrapedtitle, scrapedurl in matches:
            title = scrapedtitle.strip()
            url = urlparse.urljoin(item.url, scrapedurl)
            thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
            itemlist.append(Item(channel=__channel__, action="grabing", title=title, url=url, thumbnail=thumbnail, folder=True))
        
        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("pelisalacarta.itastreaming peliculas")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)

    patron = '<div class="item">\s*'
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
     
    #next page
    print item.url
    patternpage = "<a rel='nofollow' class=previouspostslink' href='([^']+)'>Seguente &rsaquo;</a>" 
    matches = re.compile(patternpage,re.DOTALL).findall(data)
    print matches
    
    if not matches:
        patternpage = "<span class='current'.*?</span>"
        patternpage += "<a rel='nofollow' class='page larger' href='([^']+)'>.*?</a>"
        matches = re.compile(patternpage,re.DOTALL).findall(data)
    
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=scrapedurl , folder=True) )
    
    
    return itemlist

'''# use selenium with phantomjs (phantomjs - 1.9.8 Linux x86_64 )
def grabing(item):
    logger.info("pelisalacarta.itastreaming grabing")
    itemlist = []
    if item.title:
        filmtitle = item.title
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        br = webdriver.PhantomJS(executable_path='/storage/.kodi/addons/plugin.video.pelisalacarta/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        br.get(item.url)
        br.get(item.url)
        #nData is a JS variable with films url
        nData = br.execute_script("return nData")
        for block in nData:
            #extract parametert url from list
            itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + "  quality: " + block['width'] +  " x " + block['height'] , url=block['url'] ))
        br.close()
    return itemlist
'''
def grabing(item):
    data = scrapertools.cache_page(item.url)
    logger.info("pelisalacarta.itastreaming_test grabing")
    itemlist = []
    #esegue questa funziona solo se si clicca sul titolo del film
    if item.title:
        filmtitle = item.title

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0")
        browser = webdriver.PhantomJS(executable_path='/storage/.kodi/addons/plugin.video.pelisalacarta/phantomjs',desired_capabilities = dcap, service_log_path=os.path.devnull)
        browser.get(item.url)

        try:
            nData = browser.execute_script("return nData")
            for block in nData:
                itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + "  quality: " + block['width'] +  " x " + block['height'] , url=block['url'] ))
            browser.close()

        except:
            fakeurl = re.findall('"((http)s?://www.hdpass.link.*?)"', data)
            url =  fakeurl[0][0]
            browser.get(url)
            nData = browser.execute_script("return nData")
            for block in nData:
                itemlist.append( Item(channel=__channel__, action="playit", title=filmtitle + "  quality: " + block['width'] +  " x " + block['height'] , url=block['url'] ))
            browser.close()

    return itemlist

def playit(item):
    itemlist = []
    print item.url
    itemlist.append( Item(channel=__channel__, action="playit", title=item.title , url=item.url ))
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(item.url)
    return itemlist