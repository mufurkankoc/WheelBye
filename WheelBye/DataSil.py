import sqlite3




def database_verisil():

        try:
            conn = sqlite3.connect('DEPO.db')
            cursor = conn.cursor()
            sql_emirler ='''CREATE TABLE IF NOT EXISTS LISTE(
                            PLAKA CHAR,
                            İSİM CHAR,
                            TARİH INT,
                            SAAT CHAR
                            )'''
            cursor.execute(sql_emirler)

        except:
            pass    

        giris2=str(input("Silmek istediğiniz plakayı giriniz"))
        giris2=giris2.upper()
        giris2=giris2.replace(" ", "")

        
        sil="""DELETE FROM LISTE WHERE PLAKA= '{}' """
        cursor.execute(sil.format(giris2))

            
        conn.commit()
        # conn.close()


database_verisil()