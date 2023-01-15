import sqlite3
from datetime import datetime
from bilgicek_v3 import PlateDetector
import asyncio
import websockets
import json


class Plakaci():
    # Bu Class içerisinde geçici ve kalıcı plaka bilgilerini içeren init, datayı database'e (log) yazan def.datagir
    # Json'dan sürekli plaka okuma döngüsü yapan ve plakayı seçen def.Json_Plaka_oku
    # Çıkan plaka değişkenini return eden def.getPlaka ve threading yapan def.start_reading var. 

    def __init__(self):
        self.new_plate = False
        self.plaka = ""
        self.adplayer_socket = websockets.serve(self.onPlate, '192.168.1.131', 5000)

    def datagir(self, plakaindex, aracturuindex, aracrengiindex, aracyonuindex):
        if not plakaindex.startswith('="1.0" encoding'):
            try:                                   
                conn = sqlite3.connect('LOG.db')   
                cursor = conn.cursor()                  
            except Exception:
                pass

            try:
                sql_emirler ='''CREATE TABLE IF NOT EXISTS PLAKALAR(
                    PLAKA CHAR,
                    KİŞİLER CHAR,
                    REFERANS INT,
                    ARAÇ CHAR,
                    TARİH CHAR,
                    SAAT CHAR
                    )'''
                cursor.execute(sql_emirler)
            except Exception:
                pass

            now = datetime.now()                    #Anlık Tarih ve saat çekme fonksiyonu
            dt_string = now.strftime("%d/%m/%Y")    #Tarih
            dt_string2 = now.strftime("%H:%M:%S")   #Saat
        
            ekle = """INSERT INTO PLAKALAR VALUES {}"""                                             #Database satırlarına girilecek değerler komutu
            data1 = (plakaindex, aracturuindex, aracrengiindex, aracyonuindex, dt_string, dt_string2) #Plaka,...,...,...,saat,tarih     
            cursor.execute(ekle.format(data1))

            conn.commit() #Değişiklikleri kaydet ve gir
            conn.close()  #Database kapat

    def datakontrol(self, plakaCheck):
        try:                                   
            conn = sqlite3.connect('DEPO.db')   
            cursor = conn.cursor()                  
        except Exception:
            pass

        try:
            bb = ('''SELECT İSİM from LISTE WHERE PLAKA= '{}' ''')
            cursor.execute(bb.format(plakaCheck))
            name = cursor.fetchone()[0].upper()

            conn.commit() #Değişiklikleri kaydet ve gir
            conn.close()  #Database kapat
            
            data = {
                "name": name,
                "plate": self.plaka,
                "plate_show": 1,
                "delay": 3,
            }

            return data

        except Exception:
            pass

    async def onPlate(self, websocket, path):
        while True:
            if self.new_plate:
                await websocket.send(json.dumps(self.datakontrol(self.plaka)))

                self.new_plate = False
            await asyncio.sleep(0.1)

    def plate_callback(self, plate, VehicleType, VehicleColor, VehicleDirect):
        # print(plate)
        self.new_plate = True
        self.plaka = plate
        self.aracturu = VehicleType
        self.aracrengi = VehicleColor
        self.aracyonu = VehicleDirect

        self.datagir(plate,VehicleType,VehicleColor,VehicleDirect)

        isim = self.datakontrol(plate)
        if isim is not None:
            print(isim)


        
        


plakaci = Plakaci()
asyncio.get_event_loop().run_until_complete(websockets.serve(plakaci.onPlate, '192.168.1.131', 5000))
detector = PlateDetector(plakaci.plate_callback)
detector.run()

