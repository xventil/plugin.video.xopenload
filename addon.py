#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# por DeusMaior
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

from bs4 import BeautifulSoup
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
h = HTMLParser.HTMLParser()


addon_id = 'plugin.video.xopenload'
addon_version = '0.6.2'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
base_url="https://xopenload.me/"
progress = xbmcgui.DialogProgress()

################################################## 

#MENUS############################################

def listar_categorias():
    url = base_url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all('a'):
        link = str(link)
        match = re.compile('<a href="https://xopenload.me/genre/(.+?)/">(.+?)</a>').findall(link)
        for url, name in match:
            print (url,name)
            addDir(name, base_url+'genre/'+url, 1, '')
def listar_filmes(url):
    link = str(url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(link, headers=hdr)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all('a'):
        link = str(link)
        match = re.compile('<a class="ml-mask jt" data-hasqtip="112" data-url="" href="(.+?)" oldtitle="(.+?)".+\s.+\s.+src="(.+?)"').findall(link)
        for url, name, img in match:
            addDir(name, url, 2, img)
    #for next_page in soup.find_all("a", class_="nextpostslink"):
    #    next_page = str(next_page)
    #    match = re.compile('<a class="nextpostslink" href="(.+?)" rel="next">»</a>').findall(next_page)
    #    for url in match:
    #        print ('proxima pagina '+url)
    #        addDir('Next Page >>', url, 1, '')
    #    else:
    #        print ("nao ha mais paginas")
def listar_novidades(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all("a", class_="clip-link"):
        link = str(link)
        match = re.compile('href="(.+?)" title="(.+?)">\n<.+\n<.+="(.+?)".>').findall(link)
        for url, titulo, img in match:
            addDir(titulo, url, 3, img)

    for next_page in soup.find_all("a", class_="nextpostslink"):
        next_page = str(next_page)
        match = re.compile('href="(.+?)"').findall(next_page)
        for url in match:
            addDir('Next Page >>', url, 5, '')
        else:
            print ("nao ha mais paginas")


###################################################################################
#FUNCOES


def abrir_video(video):
    #playlist = xbmc.PlayList(1)
    #title = ""
    #xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", path=video)
    #xlistitem.setInfo( "video", { "Title": title } )
    #playlist.clear()
    #playlist.add( video, xlistitem )
    video_link=str(video)
    #play_item = xbmcgui.ListItem(path=video_link)
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png",thumbnailImage='', path=video_link)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)
    xbmc.Player().play(video_link,liz)
    #try:
    #     xbmcPlayer = xbmc.Player()
         #while video.isPlayingVideo():
         #    video.TotalTime = video.getTotalTime()
         #    video.currentTime = video.getTime()
         #    watcher = (video.currentTime / video.totalTime >= .9)
         #    print (watcher)
         #xbmcPlayer.play(video)
    #     xbmcPlayer.play(playlist)
    #except:
     #    pass
      #   self.message("Erro ao abrir o video.")

def resolver_fontes(url):
    import urlresolver
    stream_url = urlresolver.resolve(url)
    abrir_video(stream_url)

def encontrar_fontes(url):
    progress.create('Play video', 'Searching videofile.')
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    req = urllib2.Request(url, headers=hdr)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, "html.parser")
    soup.find_all("a")
    soup = str(soup)
    match = re.compile('<a class="selected" href="(.+?)" id="#iframe" rel="nofollow" title=".+?">(.+?)</a>').findall(soup)
    for link, servidor in match:
        addDir(servidor, link, 4, '',False)

###################################################################################
#FUNCOES JÃ FEITAS


def abrir_url(url):
     req = urllib2.Request(url)
     req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
     response = urllib2.urlopen(req)
     link=response.read()
     response.close()
     return link

def addLink(name,url,iconimage,total,descricao):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
        liz.setInfo( type="Video", infoLabels={ "Title": name,  "Plot": descricao} )
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz, totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)




###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode==None or url==None or len(url)<1:
    listar_categorias()

elif mode==1:
    listar_filmes(url)

elif mode==2:
    encontrar_fontes(url)

#elif mode==3:
#    escolhas(url)

elif mode==4:
    resolver_fontes(url)

elif mode==5:
    listar_novidades(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))