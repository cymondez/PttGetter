#-*- encoding: utf-8 -*-
'''
Created on 2015年6月28日

@author: BigData
'''


from bs4 import BeautifulSoup

from PttDataObject import PttData

import time
import re

class PttParser(object):
    
    
    
    def __init__(self,HtmlText):
        self._soup = BeautifulSoup( HtmlText)
        self._pushTypeSwitch = {
                       u'推':'upvote',
                       u'噓':'downvote',
                       u'→':'normal'
                      }
        
        pass
    
    pass

    #(author,title,post_time,url,context)
    
    def _getUrl(self):
        for link in self._soup.select('span.f2 a'):
            if 'www.ptt.cc' in link.text :
                return link.text 
        pass
        
    def _parseArticleData(self):
        meta = self._soup.select('.article-meta-value')
        
        #加入這段保後
        if meta == None or len(meta)!=4:
            return {}
        
        username = re.sub(u' *\(.*\)',u'' ,meta[0].text)
        board=meta[1].text
        title =  meta[2].text
        time= self._parsePttTimeStr (meta[3].text)
                                
        
        url = self._getUrl();
        
        context = re.sub(u'※ 發信站: [\s\S]*','',  self._soup.select('div#main-content')[0].text )
        context = re.sub(u'(?P<meta>(作者)|(看板)|(標題)|(時間))',u'\n\g<meta> : ',  context )
        return {
                'board' : board,
                'art_author' : username ,
                'art_title': title ,
                'art_post_time' : time,
                'url' :url,
                'context': context
                }
    #  (author,push_type ,post_time,context))
    
    def _parsePushTexts(self,year):
        ls = []
        for entry in self._soup.select('.push'):
            push_type = self._transPushType( re.sub(u'[\s]',u'', entry.select('.push-tag')[0].text))
            pushid = entry.select('.push-userid')[0].text            
            pushtime = self._parserPushTimeStr ( year,entry.select('.push-ipdatetime')[0].text)
            pushcontext = re.sub(u'[\'\"]',u' ', entry.select('.push-content')[0].text[2:])
            
            data = (pushid ,push_type,pushtime ,pushcontext)
            ls.append(data)
        
        return ls

    
    #Mon Jun 29 21:40:45 2015
    
    def _parsePttTimeStr(self,timestr):
        t = time.strptime(timestr,  '%a %b %d %H:%M:%S %Y')        
        return time.strftime('%Y%m%d%H%M%S',t)
    
    def _parserPushTimeStr(self,year,timestr):
        
        t = time.strptime(year+'/'+timestr.strip(), '%Y/%m/%d %H:%M')    
        return time.strftime('%Y%m%d%H%M%S',t)
    
    def _transPushType(self,pushtag):
                        
        return self._pushTypeSwitch[pushtag ]
        
    
    def getPttData(self):
        #  author ,title ,post_time ,url ,context ,pushtxts=[]
        #{      'board' : board,
        #        'art_author' : username ,
        #        'art_title': title ,
        #        'art_post_time' : time,
        #        'url' :url
        #        'context': context
        #        }
        artData = self._parseArticleData()
        
        year = artData['art_post_time'][0:4]
        pushtxs = self._parsePushTexts(year)
        
        return PttData(artData['art_author'],artData['art_title'],
                       artData['art_post_time'],artData['url'] ,artData['context'],pushtxs)
        pass