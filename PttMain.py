# -*- coding: utf-8 -*-
'''
Created on 2015年6月22日

@author: Cymon Dez
'''
import  os
import argparse
import PttDownload as ptt
import codecs

def _getargs():
        
    defaultDir = os.environ['USERPROFILE']+'\\Documents\\ptt'#使用者的 '我的文件夾'
    
    parser = argparse.ArgumentParser(description="this is ptt loader mainj program")
    
    parser.add_argument('-s','--start',type = int,help = 'number of start loading page')
    parser.add_argument('-e','--end',type = int,help = 'number of end loading page',default=-1)
    parser.add_argument('-d','--directory',help = 'a directory which save loading files',default=defaultDir)
    parser.add_argument('-t','--delaytime',type = float,help='delay time for each link when loaded',default = 1.5)
    parser.add_argument('--errlog',type=str,help='error log file path',default=None)
    parser.add_argument('--reload',action='store_true',help='reload lost file by error log')
    parser.add_argument('--rmlog',action='store_true',help='remove error log')
    parser.add_argument('--show_downlog',action='store_true',help='show down log')

    return parser.parse_args()

def main():
    dwlogfile =   'download.log'      
    args = _getargs()
    
    if args.show_downlog :
        with codecs.open(dwlogfile,'r','utf-8') as df :
            for line in df.readlines():
                print line
            
            df.close()    
        return 
        
    print  args 
    with open(dwlogfile,'a') as f:
        f.write(str(args)+'\r\n')
        f.close()
    
    if not os.path.exists(args.directory) :
        os.makedirs(args.directory)
        
    ptt.fileSaveDirRoot = args.directory
    ptt.delaytime = args.delaytime
    
    if args.errlog != None :
        if os.path.exists(args.errlog) :
            ptt.errlogpath = args.errlog
        else :
            print u'log file {0} dose not exists '.format( args.errlog)
    
    
    if args.start !=None :    
        ptt.pageLoad(args.start, args.end)
    
    if args.reload :
        if os.path.exists(ptt.errlogpath) :
            ptt.reloadLostfile(ptt.errlogpath,args.rmlog)
        else :
            print u'log file {0} dose not exists '.format( ptt.errlogpath)
    
    #end main()
    

if __name__ == '__main__':
    main()