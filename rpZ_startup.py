from rpZ_LTEStart import rpZ_LTEStart
import rpConnectZero
import asyncio
import rpZ_LTEStart
import dotenv
import http.client
import json

class rpZ_startup():
    async def __init__(self):
        try:
            _rpZLTEConnected = await rpZ_LTEStart.rpZ_LTEStart()
            if _rpZLTEConnected:
                _rpPico_COM = rpConnectZero.rpConnectZero()
                _rpPico_COM.RX_data()
                self.data = _rpPico_COM.handshake.data
                print(self.data)
        except:
            print('R2D2 Scream')
        finally:
            conn = http.client.HTTPSConnection(dotenv.lambdaURI)
            payload = json.dumps({
                "id": "2",
                "record": self.data
            })
            headers = {
                'x-api-key': dotenv.xapikey,
                'piGPS_webhook-Key': dotenv.piGPS_webhookKey,
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/default/piGPS_webhook", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))