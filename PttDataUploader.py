#-*- encoding: utf-8 -*-
'''
Created on 2015年6月28日

@author: BigData
'''

import MySQLdb as sql

import PttDataObject



class MySqlLinker(object):
    
    
    def __init__(self ,host = 'localhost',port = 3306,dbname = '',user = 'root',password = '',useUnicode = True):
        if useUnicode :
            self._db = sql.connect (host,user,password,dbname,charset='utf8')
        else :
            self._db = sql.connect (host,user,password,dbname)
            
        
        pass
        
        
    
    def __del__(self):
        self._db.close()
        pass
    
    
    
    
    def upload(self,pttdata):
        if  not isinstance(pttdata,PttDataObject.PttData) :
            raise Exception('type error')
        
        
        cursor = None
        crntAutoIncrement = 0
                
        try :

            
            cursor = self._db.cursor()
            
            
            self.uploadArticle( pttdata.getartdata(), cursor, commit = False)        
            
            
            pushtxts = pttdata.getpushtxts()
            if len(pushtxts) != 0 :
                
                crntAutoIncrement = self._getCrntAutoIncrement(cursor) 
                                       
                self.uploadPushTexts(crntAutoIncrement ,pushtxts ,cursor ,commit = False )
            
                        
            self._commit()
                        
        
        except sql.Error as myerr:
            #clear auto increment  
            self._resetAutoIncrement(cursor,value= crntAutoIncrement-1 )
            raise myerr
            
        #except Exception as e:
        #    print e
        #    raise e
            
        finally:
            if cursor :
                cursor.close()
        pass

    
    def uploadArticle(self ,artData ,cursor = None ,commit = True):
        
        isoutCursor = False
        if cursor != None :
            cursor = self._db.cursor()
            isoutCursor = True
        
        old_increment = self._getCrntAutoIncrement(cursor)
        
        try :
            insertCmd = """ insert into article (author,title,post_time,url,context)
            values (%s,%s,%s,%s,%s) """
            cursor.execute(insertCmd,artData)

            
            if not isoutCursor :
                self._commit()
        except sql.Error as sqlerr:
            if not isoutCursor :
                #clear auto increment  
                self._resetAutoIncrement(cursor, old_increment)
            raise sqlerr
        finally:
            if not isoutCursor :
                cursor.close()
            
            
        
        pass
    
    def uploadPushTexts(self,art_id ,pushtexts = [] ,cursor=None ,commit = True):
        isoutCursor = False
        if cursor != None :
            cursor = self._db.cursor()
            isoutCursor = True
                
        try :
            ls =[ (art_id,)+x for x in pushtexts]
            print ls[0]
            insertCmd = """ insert into pushtxt (art_id, author,push_type ,post_time,context)
            values (%s, %s, %s, %s, %s) """
            cursor.executemany(insertCmd,ls)

            
            if not isoutCursor :
                self._commit()
        finally:
            if not isoutCursor :
                cursor.close()
            
            
        
        pass
    
    def _getCrntAutoIncrement(self,cursor):
        qureyCmd = "SELECT `auto_increment`-1 FROM INFORMATION_SCHEMA.TABLES where table_name = 'article'"
        cursor.execute(qureyCmd)
        crntAutoIncrement = cursor.fetchone()[0] #return val is a tuple!!
        return crntAutoIncrement
    
    def _resetAutoIncrement(self,cursor,value = 0):
        
        qureyCmd = "ALTER TABLE article AUTO_INCREMENT=" + str(value)
        
        cursor.execute(qureyCmd)
    
    def _commit(self):
        self._db.commit() 
        
    
    
    
    pass
