from typing import final
import pyhik.hikvision as hikvision
import asyncio
import json
import websockets
import time

class VehicleInfo:
    def findPlate(xml):
        start = xml.find("<licensePlate>") + len("<licensePlate>")
        end = xml.find("</licensePlate>")
        plate = xml[start:end]
        return plate

    def findVehicleType(xml):
        start = xml.find("<vehicleType>") + len("<vehicleType>")
        end = xml.find("</vehicleType>")
        Type = xml[start:end]
        return Type

    def findVehicleColor(xml):
        start = xml.find("<color>") + len("<color>")
        end = xml.find("</color>")
        Color = xml[start:end]
        return Color

    def findVehicleDirect(xml):
        start = xml.find("<direction>") + len("<direction>")
        end = xml.find("</direction>")
        Color = xml[start:end]
        return Color



class PlateDetector:
    def __init__(self, callback = None):
        self.token = None
        self.camHost = "192.168.1.64"
        self.cam = hikvision.HikCamera(f'http://{self.camHost}', 80, 'admin', 'Solid321')
        self.callback = callback
        

    def refresh_token(self):
        try:
            response = self.cam.hik_request.get(self.cam.root_url + "/ISAPI/Security/token?format=json")
            resobj = json.loads(response.text)
            self.token = resobj["Token"]["value"]
        except Exception as e:
            print(e)

    async def listen_ws(self):
        while True: 
            try:
                uri = f"ws://{self.camHost}:7681/ISAPI/Event/notification/subscribeEventCap?token=" + self.token
                async with websockets.connect(uri) as websocket:
                    greeting = await websocket.recv()
                     
                    with open('hikmessage.xml', 'r') as file:
                        init = file.read().replace('\n', '')
                        await websocket.send(init)
                        
                    
                    while True: # plaka loop
                        greeting = await websocket.recv()
                        if type(greeting)is str and greeting.startswith('<?xml version="1.0"'):                           
                            InfoClass = VehicleInfo
                            plate = VehicleInfo.findPlate(greeting)
                            VehicleType = VehicleInfo.findVehicleType(greeting)
                            VehicleColor = VehicleInfo.findVehicleColor(greeting)
                            VehicleDirect= VehicleInfo.findVehicleDirect(greeting)

                            if self.callback is not None:
                                self.callback(plate,VehicleType,VehicleColor,VehicleDirect)


            except Exception as e:
                print(e)
                self.refresh_token()
            
            # time.sleep(1)

    def run(self):
        self.refresh_token()
        asyncio.get_event_loop().run_until_complete(self.listen_ws())
        


       
