#-*- encoding: utf-8 -*-
'''
Created on 2015年6月30日

@author: BigData
'''

from __future__ import print_function


import os 
import codecs

from PttParser import PttParser
from PttDataUploader import MySqlLinker

import argparse
import uuid


success_cnt = 0

def uploadfiles(dir_path,recursive = True,host = 'localhost',port = 3306,dbname = '',user = 'root',password = '',useUnicode = True):
    #host = 'localhost',port = 3306,dbname ,user = 'root',password = '',useUnicode = True):
    global success_cnt
    sqlLinker = None
    
    try:
        sqlLinker  = MySqlLinker(host,port,dbname,user,password)

        _uploadfile(dir_path, sqlLinker,recursive)
    finally:
        if sqlLinker :
            del sqlLinker
        print ("success count : {0}".format(success_cnt)) 
        success_cnt = 0
    

def _uploadfile(dir_path,sqlLinker,recursive = True):
    
    global success_cnt
    
    if not os.path.isdir(dir_path) :
        raise Exception('"{0}" is not a dirctory path !'.format(dir_path))
    
    
    for filename in os.listdir(dir_path):
        
        fullname = os.path.join(dir_path,filename)
        
        if os.path.isdir(fullname) and recursive:
            _uploadfile(fullname, sqlLinker,recursive)
        
        elif os.path.isfile(fullname):
            try :
                print (u'uploadfile : {0}'.format(fullname) ,end = ' ')
                with codecs.open(fullname,'r','utf-8') as f :
                    parser = PttParser(f.read())
            
                    data = parser.getPttData()
                    sqlLinker.upload(data)
                print (u'+OK')
                success_cnt += 1
            except Exception as e:
                print (u'-Error')                
                _writelog(u'[update lost]{0}[reson]{1}'.format(fullname,e))
                pass
            finally:
                pass
            pass
        
        else :
            print ('{0} is not file or directory !'.format(fullname))


_logfile = 'errlog.log'
def _writelog(msg):
    with codecs.open(_logfile,'a','utf-8') as f :
        print (msg ,file = f) 
        f.close()
         
    
def _getargs():
        
    defaultDir = os.environ['USERPROFILE']+'\\Documents\\ptt'#使用者的 '我的文件夾'
    
    parser = argparse.ArgumentParser(description="this is ptt loader mainj program")
    
    parser.add_argument('--host',type=str,help = 'sql host',default='localhost')
    parser.add_argument('-u','--user',type=str,help = 'sql user name',default='root')
    parser.add_argument('-p','--password',type=str,help = 'sql user password')
    parser.add_argument('--database',type=str,help = 'database name which will be uploading to ',default='ptt')
    parser.add_argument('--port',type = int,help = 'sql port',default=3306)
    parser.add_argument('-d','--directory',help = 'a directory which will be uploading files',default=defaultDir)
    parser.add_argument('-r','--recursive',action='store_true',help='recursive dirctory to uplaod files')
    parser.add_argument('--errlog',type=str,help='error log file path',default='errlog.log')
#     parser.add_argument('-m','--move_uploaded_file',action='store_true',help='move uploaded files to already directory')
#     parser.add_argument('--already_dir',help = 'a directory which save uploaded files',default= os.path.join( os.path.dirname(defaultDir),'old_ptt' ))
#     #parser.add_argument('--rmlog',action='store_true',help='remove error log')

    return parser.parse_args()


def main():
    args = _getargs()
    print (args) 
    
    dir_path = u'%s'%args.directory;
    if not os.path.exists(dir_path) :
        raise Exception('dirctory not exists !') 
    host = args.host
    port = args.port
    user = args.user
    password = args.password
    dbname = args.database
    recursive = True if args.recursive else False
    
    try :
        uploadfiles(dir_path, recursive, host, port, dbname, user, password, True)
    except Exception as e:
        print (e)
    
    pass

if __name__ == '__main__':
    main()