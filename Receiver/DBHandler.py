import psycopg2
import datetime
from datetime import datetime, timezone



class DBHandler:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="smartgarden",
                user="pi",
                password="oenikbrr123")
        except:
            print ("DB NOT FOUND")
        self.cur = self.conn.cursor()
    
        
        
        
        

    def Write(self,soil,temp):
        dt = datetime.now()
        self.cur.execute("insert into espdata (id, created, soil,temperature) values (NEXTVAL('espdata_id_seq'),%s, %s, %s)", (dt,soil, temp) )
        self.conn.commit()

    def Disconnect(self):
        self.cur.close()
        self.conn.close()


#d = DBHandler()
#d.Write(600,24)
#d.Disconnect()
#print ("DONE")