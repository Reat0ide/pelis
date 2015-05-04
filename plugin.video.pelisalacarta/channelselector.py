# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist():
    logger.info("channelselector.getmainlist")
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("channelselector.getmainlist idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]
    
    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118)+" ("+idiomav+")" , channel="channelselector" , action="channeltypes", thumbnail = urlparse.urljoin(get_thumbnail_path(),"channelselector.png") ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(),"buscador.png")) )
    itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(),"trailertools.png")) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(),"favoritos.png")) )
    if config.get_platform() in ("wiimc","rss") :itemlist.append( Item(title="Wiideoteca (Beta)" , channel="wiideoteca" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"wiideoteca.png")) )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(),"pyload.png")) )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"descargas.png")) )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"configuracion.png"), folder=False) )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"configuracion.png")) )

    #if config.get_setting("fileniumpremium")=="true":
    #	itemlist.append( Item(title="Torrents (Filenium)" , channel="descargasfilenium" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"torrents.png")) )

    #if config.get_library_support():
    if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"ayuda.png")) )
    return itemlist

# TODO: (3.1) Pasar el código específico de XBMC al laucher
def mainlist(params,url,category):
    logger.info("channelselector.mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("channelselector.mainlist No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("channelselector.mainlist Verificar actualizaciones activado")
                try:
                    updater.checkforupdates()
                except:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    dialog.ok("No se puede conectar","No ha sido posible comprobar","si hay actualizaciones")
                    logger.info("channelselector.mainlist Fallo al verificar la actualización")
                    pass
            else:
                logger.info("channelselector.mainlist Verificar actualizaciones desactivado")

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("channelselector.mainlist item="+elemento.title)
        addfolder(elemento.title , elemento.channel , elemento.action , thumbnail=elemento.thumbnail, folder=elemento.folder)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def getchanneltypes():
    logger.info("channelselector getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"channelselector")))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"peliculas")))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"series")))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"anime")))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"documentales")))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail=urlparse.urljoin(get_thumbnail_path(),"versionoriginal")))
    itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"musica")))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail=urlparse.urljoin(get_thumbnail_path(),"servidores")))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail=urlparse.urljoin(get_thumbnail_path(),"novedades")))
    return itemlist
    
def channeltypes(params,url,category):
    logger.info("channelselector.mainlist channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,item.category,item.thumbnail,item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listchannels(params,url,category):
    logger.info("channelselector.listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            if channel.channel=="personal":
                thumbnail=config.get_setting("personalchannellogo")
            elif channel.channel=="personal2":
                thumbnail=config.get_setting("personalchannellogo2")
            elif channel.channel=="personal3":
                thumbnail=config.get_setting("personalchannellogo3")
            elif channel.channel=="personal4":
                thumbnail=config.get_setting("personalchannellogo4")
            elif channel.channel=="personal5":
                thumbnail=config.get_setting("personalchannellogo5")
            else:
                thumbnail=channel.thumbnail
                if thumbnail == "":
                    thumbnail=urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def filterchannels(category):
    returnlist = []

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            channel.thumbnail = urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)
    else:
        try:
            idioma = config.get_setting("languagefilter")
            logger.info("channelselector.filterchannels idioma=%s" % idioma)
            langlistv = ["","ES","EN","IT","PT"]
            idiomav = langlistv[int(idioma)]
            logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
        except:
            idiomav=""

        channelslist = channels_list()
    
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en la categoría elegida
            if category<>"*" and category not in channel.category:
                #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
                continue
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            if channel.thumbnail == "":
                channel.thumbnail = urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    itemlist = []
    itemlist.append( Item( title="Newpct (08/03/2013)"               , channel="newpct"          , language="ES"    , category="F,S,D,A"       , type="generic"  )) # jesus 08/03/2013
    itemlist.append( Item( title="Malvin.tv (12/02/2013)"            , channel="malvin"          , language="ES"    , category="F,D"       , type="generic"  )) 
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PelisX (01/02/2013)"               , channel="pelisx"          , language="ES"    , category="F"       , type="generic"  )) # ZeDinis 01/02/2013
    itemlist.append( Item( title="Nukety (25/12/2012)"               , channel="nukety"          , language="ES"    , category="F,S"       , type="generic"  )) 
    itemlist.append( Item( title="Film per tutti (IT) (27/11/2012)"  , channel="filmpertutti"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="Watch Cartoon Online (23/11/2012)" , channel="watchcartoononline"   , language="EN" , category="F,S", type="generic" )) # jesus 23/11/2012
    itemlist.append( Item( title="Series Online TV (12/11/2012)"     , channel="seriesonlinetv", language="ES" , category="S" , type="generic"  )) # jesus 12/11/2012
    itemlist.append( Item( title="Novelas de TV (12/11/2012)"        , channel="novelasdetv", language="ES" , category="S" , type="generic"  )) # jesus 12/11/2012
    itemlist.append( Item( title="Quiero Dibujos Animados (12/11/2012)", channel="quierodibujosanimados", language="ES" , category="S" , type="generic"  )) # jesus 12/11/2012
    #itemlist.append( Item( title="Cinemastreaming (IT) (5/11/2012)"  , channel="cinemastreaming"      , language="IT" , category="F,S,A" , type="generic"  )) # jesus 5/11/2012
    itemlist.append( Item( title="Peliculamos (IT) (5/11/2012)"      , channel="peliculamos"          , language="IT" , category="F,S,A" , type="generic"  )) # jesus 5/11/2012
    itemlist.append( Item( title="JKanime (15/10/2012)"              , channel="jkanime"              , language="ES" , category="A" , type="generic"  )) # jesus 15/10/2012
    itemlist.append( Item( title="Ver Telenovelas (15/10/2012)"      , channel="vertelenovelas"       , language="ES" , category="S" , type="generic"  )) # jesus 15/10/2012
    itemlist.append( Item( title="Yaske.net (09/10/2012)"            , channel="yaske"                , language="ES" , category="F" , type="generic"    )) # jesus 09/10/2012
    itemlist.append( Item( title="Divxatope (27/08/2012)"            , channel="divxatope"            , language="ES" , category="F,S" , type="generic"    )) # jesus 27/08/2012
    itemlist.append( Item( title="Mejortorrent (20/08/2012)"         , channel="mejortorrent"         , language="ES" , category="F,S" , type="generic"    )) # jesus 20/08/2012
    itemlist.append( Item( title="Newdivxonline (07/08/2012)"        , channel="newdivxonline"        , language="ES" , category="F" , type="generic"    )) # morser 07/08/2012
    itemlist.append( Item( title="cine-online.eu (16/07/2012)"       , channel="cineonlineeu"         , language="ES" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Pirate Streaming (16/07/2012)"     , channel="piratestreaming"      , language="IT" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Tucinecom (16/07/2012)"            , channel="tucinecom"            , language="ES" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Cinetux (16/07/2012)"              , channel="cinetux"              , language="ES" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Tus Novelas (03/07/2012)"          , channel="tusnovelas"           , language="ES" , category="S" , type="generic"    )) # jesus 3/7/2012
    itemlist.append( Item( title="Unsoloclic (03/07/2012)"           , channel="unsoloclic"           , language="ES" , category="F,S" , type="generic"  )) # jesus 3/7/2012
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Cinetemagay (15/04/2012)"          , channel="cinetemagay"          , language="ES" , category="F" , type="generic"    )) # sdfasd 15/4/2012
    itemlist.append( Item( title="Sipeliculas (02/03/2012)"          , channel="sipeliculas"          , language="ES" , category="F" , type="generic"    )) # miguel 2/3/2012
    itemlist.append( Item( title="Gnula (15/12/2011)"                , channel="gnula"                , language="ES" , category="F" , type="generic"  )) # vcalvo 15/12/2011
    itemlist.append( Item( title="Series ID (15/12/2011)"            , channel="seriesid"             , language="ES" , category="S,VOS" , type="generic"  )) # vcalvo 15/12/2011
    itemlist.append( Item( title="Bajui (14/12/2011)"                , channel="bajui"                , language="ES" , category="F,S,D,VOS", type="generic")) # vcalvo 14/12/2011
    itemlist.append( Item( title="Shurweb (14/12/2011)"              , channel="shurweb"              , language="ES" , category="F,S,D,A", type="generic")) # vcalvo 14/12/2011
    itemlist.append( Item( title="Justin.tv (12/12/2011)"            , channel="justintv"             , language=""   , category="G"       , type="generic"  )) # bandavi 12/12/2011
    itemlist.append( Item( title="Series.ly (19/11/2011)"            , channel="seriesly"             , language="ES" , category="S,A,VOS" , type="generic" )) # jesus/mrfloffy 19/11/2011
    itemlist.append( Item( title="Teledocumentales (19/10/2011)"     , channel="teledocumentales"     , language="ES" , category="D" , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="Peliculasaudiolatino (14/10/2011)" , channel="peliculasaudiolatino" , language="ES" , category="F"   , type="generic" )) # Dalim 14/10/2011
    itemlist.append( Item( title="Animeflv (14/10/2011)"             , channel="animeflv"             , language="ES" , category="A,VOS"   , type="generic" )) # MarioXD 14/10/2011
    itemlist.append( Item( title="Moviezet (01/10/2011)"             , channel="moviezet"             , language="ES" , category="F,S,VOS" , type="generic" )) # mrfluffy 01/10/2011
    #itemlist.append( Item( title="NewHD (05/05/2011)"                , channel="newhd"                , language="ES" , category="F"   , type="generic" )) # xextil 05/05/2011
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Serviporno (16/02/2015)"          , channel="serviporno"          , language="ES" , category="F" , type="generic"    ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Serviporno (17/02/2015)"          , channel="serviporno"          , language="ES" , category="F" , type="generic"    ))
    return itemlist

def channels_list():
    itemlist = []
    
    

    itemlist.append( Item( viewmode="movie", title="Tengo una URL"         , channel="tengourl"   , language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname") , channel="personal" , language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname2") , channel="personal2" , language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname3") , channel="personal3" , language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname4") , channel="personal4" , language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname5") , channel="personal5" , language="" , category="F,S,D,A" , type="generic"  ))
    
    itemlist.append( Item( title="Cineblog01 (IT)"       , channel="cineblog01"           , language="IT"    , category="F,S,A,VOS"   , type="generic"  ))
    itemlist.append( Item( title="Film per tutti (IT)"      , channel="filmpertutti"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="Film Senza Limiti (IT)"        , channel="filmsenzalimiti"       , language="IT"    , category="F"       , type="generic"     ))
    itemlist.append( Item( title="ItaliaFilms.tv (IT)"      , channel="italiafilm"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="Itastreaming (IT)"      , channel="itastreaming"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="Pirate Streaming (IT)" , channel="piratestreaming"      , language="IT" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Robinfilm (IT)"        , channel="robinfilm"            , language="IT" , category="F"          , type="generic"  )) # jesus 16/05/2011
    itemlist.append( Item( title="Serie TV Sub ITA"          , channel="serietvsubita"         , language="IT" , category="S"        , type="generic" , extra="Series" ))
    itemlist.append( Item( title="Griffin Ita"          , channel="griffin"         , language="IT" , category="F,S,D,A"        , type="generic" ))
    itemlist.append( Item( title="Itastreaming_test"          , channel="itastreaming_test"         , language="IT" , category="F,S,D,A"        , type="generic" ))
    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)

def get_thumbnail_path():

    WEB_PATH = ""
    
    thumbnail_type = config.get_setting("thumbnail_type")
    if thumbnail_type=="":
        thumbnail_type="2"
    
    if thumbnail_type=="0":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/posters/"
    elif thumbnail_type=="1":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/banners/"
    elif thumbnail_type=="2":
        WEB_PATH = "http://pelisalacarta.mimediacenter.info/squares/"

    return WEB_PATH
