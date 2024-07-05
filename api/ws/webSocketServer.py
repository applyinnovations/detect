#!/usr/bin/env python

import asyncio
from websockets import WebSocketServerProtocol
from websockets.server import serve

connected_clients = set()

class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = int(port)

    async def handler(self, websocket:WebSocketServerProtocol):
    
        connected_clients.add(websocket)
        
        async for message in websocket:
            for client in connected_clients:
                if(client.open):
                    await client.send(message)    
            

    async def main(self):
        async with serve(self.handler,self.host, self.port):
            await asyncio.Future()  # run forever
            
    def start(self):
        print('calling web sockets')
        asyncio.run(self.main())