#-*- encoding: utf-8 -*-
'''
Created on 2015年6月29日

@author: BigData
'''



import os 
import codecs


from PttParser import PttParser
from PttDataUploader import MySqlLinker

import MySQLdb

def testParser():
    
    root = u'E:\\ptt_all_data\\01.ptt_old\\PTT'#u'E:/PTT'
    filelist = []
    for filename in os.listdir(root) :
        filelist.append( os.path.join(root,filename))
    
    with codecs.open(filelist[0],'r','utf-8') as f :
        parser = PttParser(f.read())
        
        data = parser.getPttData()
        print data.showdata()
        
        return data    
            
def testUplaod():
    #host = 'localhost',port = 3306,dbname ,user = 'root',password = '',useUnicode = True):
    try:
        linker  = MySqlLinker(host = '10.120.31.5',port = 3306,dbname='ptt',user = 'zb101',password='zb101')
        linker.upload(testParser())
    finally:
        del linker
    pass

testParser()
#testUplaod()


