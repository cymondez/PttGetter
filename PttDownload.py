# -*- coding: utf-8 -*-
'''
Created on 2015年6月22日

@author: Cymon Dez

'''
import os
        
import re
import time
#import requests
import requests.packages
from bs4 import BeautifulSoup

import codecs

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()


#public
fileSaveDirRoot = 'D:\\PTT'
errlogpath = os.environ['USERPROFILE']+'\\Documents\\pttload.log'
delaytime = 1.5

#private
lostfiletag = '[file lost]'

def _errlog(msg,filename=None):
    if filename == None :
        filename = errlogpath
        
    msg ='[{0}]'.format(time.strftime('%y-%m-%d %H:%M:%S'))+ str(msg)+'\n------------------------------\n'
    try:
        with open(filename,'a') as f:
                f.write(msg)
                f.close()
    except Exception as e:
        print e 

def createFilename(title ,author ,datetime,extension = 'txt'): 
    
    
    rt = u'[Title]{0}[Author]{1}[Date]{2}.{3}'.format(title,author,datetime,extension)
    return re.sub(r'[:/\\*?"|<>]','-',rt) #將不合法路徑字元用 '-'號取代

def _getInfo(soup):
    meta = soup.select('.article-meta-value')

    title = unicode(meta[0].text)
    #board =  meta[1].text
    username= unicode( meta[2].text)
    time =  unicode(meta[3].text)
    #content = soup.select('#main-content')[0].text

    
    return {'author':username,
            'title':title,
            'datetime':time,
            }

def _saveContent(path,info,content):

    fname = createFilename(info['author'],info['title'],info['datetime'])
    
    filename=  unicode( os.path.join(path,fname) )

    
    with open(filename,'w') as f :
        f.write(content)
        f.close()
    print filename

def _contentLinkLoadByUrl(rs,url):
    
    try:
        res = rs.get('https://www.ptt.cc/' +url)
        soup = BeautifulSoup(res.text)
        meta = soup.select('.article-meta-value')
        if meta == None or len(meta)!=4:
            return False
                    
                        
        content = (res.text).encode('utf-8')
        path = fileSaveDirRoot
        info  = _getInfo(soup)
        _saveContent( path,info,content)
        
        return True
                    
    #exception by content link    
    except Exception as e:
        print u'{0}'.format(e)
        #_errlog(e)
        return False
    

def _contentLinkLoad(rs,link):
    url =  link['href']
    return _contentLinkLoadByUrl(rs,url)



def pageLoad(start,end=-1):
    '''
    payload={'from':'/bbs/Gossiping/index.html','yes':'yes'}
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html', verify=False)
    
    soup = BeautifulSoup(res.text)
    pageurl = soup.select('.wide')[1]['href']
    '''   
    cnt = long(0) # load file counter
    err_cnt  = long(0) #lost file counter
    
    #over18 verify  
    payload={'from':'/bbs/Gossiping/index.html','yes':'yes'}
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    
    #get the max page number
    soup = BeautifulSoup(res.text)
    pageurl = soup.select('.wide')[1]['href']
    maxpage = int(pageurl.split('index')[1].split('.html')[0])
    #check end boundary    
    if end == -1 or end > maxpage:
        end = maxpage
    
    #load pages 
    for cntPage in range(start,end+1): 
        try:
            print 'loading page {0}'.format(cntPage)
            res = rs.get('https://www.ptt.cc/bbs/Gossiping/index%d.html'%(cntPage), verify=False)
            soup = BeautifulSoup(res.text)   
            
            #load content in page
            for link in soup.select('.r-ent a'):
                
                if _contentLinkLoad(rs,link) :
                    cnt+=1
                else :
                    err_cnt+=1 
                    _errlog(lostfiletag+' href={0} page={1}'.format(link,cntPage))
                
                time.sleep(delaytime) #為避免過度qurey PTT Server 
                    
            print 'load end page {0}'.format(cntPage)
            print '--------------------------------------------------'
        #exception by page
        except Exception as e: 
            print u'{0}'.format(e)
            _errlog('[page lost] page={0}\n\t msg={1}'.format(cntPage,e) )
             
    print 'mission completed ! total  : {0} ,lost :{1}'.format(cnt,err_cnt)


def dayLoad(st_day,end_day):
    pass

def _getlostfileLinkInfos(logpath):
    links=[]
    with codecs.open(logpath,'r','utf-8') as f:
        txt = f.read()        
        matchs = re.findall('\[file lost\] href=\<a href="(?P<url>.*)"\>(?P<title>.*)\</a\>',txt)
        for m in matchs :
            links.append({'url':m[0],'title':m[1]})
        f.close()
    return links

def reloadLostfile(logpath,rmlog=False):
    infos = _getlostfileLinkInfos(logpath)

    relen = len(infos)
    if relen == 0 :
        print 'Nothing to reload !'
        return 
    
    if rmlog:    
        os.remove(logpath)
    
    cnt = long(0) # load file counter
    err_cnt  = long(0) #lost file counter
    
    #over18 verify  
    payload={'from':'/bbs/Gossiping/index.html','yes':'yes'}
    rs = requests.session()
    rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    print 'total {0} begin reload'.format(relen)
    for info in infos :
        
        print u'reload {0}'.format(info['title'])
        if    _contentLinkLoadByUrl(rs,info['url']):
            cnt+=1
        else:
            err_cnt+=1 
            _errlog('[reload fault] href={0} '.format(info['url']) )
        
        time.sleep(delaytime) #為避免過度qurey PTT Server
    print 'already reload : {0} ,lost : {1}'.format(cnt,err_cnt)
    
    
if __name__ == '__main__' :
    
    pageLoad(64,64)
