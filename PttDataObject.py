#-*- encoding: utf-8 -*-
'''
Created on 2015年6月28日

@author: BigData
'''

#import time

class PttData(object):
    
    def __init__(self,  author ,title ,post_time ,url ,context ,pushtxts=[]):
        self.author = author
        self.title = title
        self.post_time = post_time
        self.url = url
        self.context = context
        
        if pushtxts :
            self.pushtxts = pushtxts
        else :
            self.pushtxts = []
        pass
    
    
    def showdata(self):
        print u'文章'
        print u'作         者 :', self.author 
        print u'標         題 :',self.title
        print u'發文時間 :',self.post_time 
        print u'URL :',self.url 
        print u'內文:\n',self.context 
        print u'    ------推文-----    '
        for p in self.pushtxts :
            #(pushid ,push_type,pushtime ,pushcontext)
            print u"{1} : {3}  |{2}".format(*p)
        
        pass
    

    def getartdata(self):
        artData = (self.author,self.title, self.post_time ,self.url,self.context)
        return artData
    
    def getpushtxts(self):
        
        return self.pushtxts
        