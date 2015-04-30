# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para itastreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import json
   

__channel__ = "griffin"
__category__ = "F"
__type__ = "generic"
__title__ = "griffin"
__language__ = "IT"

DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"
def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.griffin  mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 1" , url="http://griffinita.altervista.org/stagioni/stagione-1" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 2" , url="http://griffinita.altervista.org/stagioni/stagione-2" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 3" , url="http://griffinita.altervista.org/stagioni/stagione-3" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 4" , url="http://griffinita.altervista.org/stagioni/stagione-4" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 5" , url="http://griffinita.altervista.org/stagioni/stagione-5" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 6" , url="http://griffinita.altervista.org/stagioni/stagione-6" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 7" , url="http://griffinita.altervista.org/stagioni/stagione-7" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 8" , url="http://griffinita.altervista.org/stagioni/stagione-8" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 9" , url="http://griffinita.altervista.org/stagioni/stagione-9" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 10" , url="http://griffinita.altervista.org/stagioni/stagione-10" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 11" , url="http://griffinita.altervista.org/stagioni/stagione-11" ))
    itemlist.append( Item(channel=__channel__ , action="peliculas", title="Stagione 12" , url="http://griffinita.altervista.org/stagioni/stagione-12" ))
    
    return itemlist



#azione "peliculas" server per estrerre i titoli
def peliculas(item):
    logger.info("pelisalacarta.griffin peliculas")
    itemlist = []
    # Descarga la pagina
    
    data = scrapertools.cache_page(item.url)
    
    patron  = '<h3 class="catItemTitle">\s*'
    patron += '<a href="?([^>"]+)"?'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    print matches
    
    #create title from url
    for result in matches:
		url='http://griffinita.altervista.org'
		url+=''.join(result)
		title=''.join(result)
		title=title[1:]
		itemlist.append( Item(channel=__channel__, action="playit", title=title , url=url, folder=True) )
	
    return itemlist


def playit(item):
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    
    '''
    <div class="itemFullText">
    <p><iframe height="400" src="https://docs.google.com/file/d/0B1uREFqXSZCZVVh5SnM4Y2pqeWc/preview" allowfullscreen="1" webkitallowfullscreen="1" width="100%"></iframe></p>	  </div>
    '''                                        	  	
    pattern = '<div class="itemFullText">\s*'
    pattern += '<p><iframe height="400" src="?([^>"]+)"?'
    decodedurl = re.compile(pattern,re.DOTALL).findall(data)
    decodedurl = ''.join(decodedurl)
    decodedurl+= '?autoplay=1'
    itemlist.append( Item(channel=__channel__, action="playit", title=item.title , url=item.url ))
    googleurl='plugin://plugin.video.gdrive?mode=streamURL&amp;url='
    googleurl+=decodedurl
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(googleurl)
        
    return itemlist

