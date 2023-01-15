import sqlite3


def database_verigir():
   

   conn = sqlite3.connect('Depolama.db')

   cursor = conn.cursor()

   cursor.execute("INSERT INTO PLAKALAR VALUES(?,?,?,?)",("A","B",1,"C"))
      
      
   conn.commit()
   # conn.close()


database_verigir()




