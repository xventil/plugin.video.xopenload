#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import sys
import xbmc, xbmcgui, xbmcplugin
import urllib, urlparse
import requests, re
import urlresolver

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
top_url = 'https://xopenload.me/'
progress = xbmcgui.DialogProgress()

args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent (addon_handle,'videos')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)


def get_categories():
    url = top_url
    mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    r = requests.get(url, headers = mozhdr)
    soup = BeautifulSoup(r.content, "html.parser")
    for link in soup.find_all('a'):
        link = str(link)
        match = re.compile('<a href="https://xopenload.me/genre/(.+?)/">(.+?)</a>').findall(link)
        for url, name in match:
            li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png')
            url = str('https://xopenload.me/genre/'+url)
            url = build_url({'mode':'categorias','foldername':name,'videolink':url})
            xbmcplugin.addDirectoryItem(handle=addon_handle,url = url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
               
def get_videos(url):
    mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    r = requests.get(url, headers = mozhdr)
    soup = BeautifulSoup(r.content, "html.parser")
    for link in soup.find_all('a'):
        link = str(link)
        match = re.compile('<a class="ml-mask jt" data-hasqtip="112" data-url="" href="(.+?)" oldtitle="(.+?)".+\s.+\s.+src="(.+?)"').findall(link)
        for url, name, img in match:
            li = xbmcgui.ListItem(name, iconImage=img)
            url = str(url)
            url = build_url({'mode':'videos','foldername':name,'videolink':url,'image':img})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def play_videos(link):
    play_item = xbmcgui.ListItem(path=link)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    play_item.setPath(str(stream_url))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=play_item)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:
        return stream_url    

def encontrar_fontes(fonte):
    mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    r = requests.get(fonte, headers = mozhdr)
    soup = BeautifulSoup(r.content, "html.parser")
    soup.find_all("a")
    soup = str(soup)
    match = re.compile('<a class="selected" href="(.+?)" id="#iframe" rel="nofollow" title=".+?">(.+?)</a>').findall(soup)
    for link, servidor in match: 
        li = xbmcgui.ListItem(servidor, iconImage='DefaultFolder.png')
        url = str(link)
        url = build_url({'mode':'fontes','foldername':servidor,'videolink':url})
        li.setProperty('IsPlayable' , 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)



if mode is None:
    get_categories()

elif mode[0] == 'categorias':
    url = args['videolink'][0]
    get_videos(url)

elif mode[0] == 'videos':
    fonte = args['videolink'][0]
    encontrar_fontes(fonte)


elif mode[0] == 'fontes':
    link = args['videolink'][0]
    play_videos(link)

else:
    print('já nem sei onde estou...')
