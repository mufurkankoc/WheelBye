import sqlite3


def database_verigir(xxx):
    plakaverisi=xxx
   
    try:
        conn = sqlite3.connect('DEPO.db')

        cursor = conn.cursor()


        bb=('''SELECT İSİM from LISTE WHERE PLAKA= '{}' ''')

        cursor.execute(bb.format(plakaverisi))
        

        result=cursor.fetchone()[0]
        

        ayt=result.upper()

        conn.commit() #Değişiklikleri kaydet ve gir
        conn.close()  #Database kapat

    except:

        ayt="plaka yok"

    return ayt

print(database_verigir("38an476"))
    
