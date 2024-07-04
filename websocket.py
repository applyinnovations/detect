#!/usr/bin/env python

import asyncio
from websockets import WebSocketServerProtocol
from websockets.server import serve

connected_clients = set()

async def echo(websocket:WebSocketServerProtocol):
    
    connected_clients.add(websocket)
    
    async for message in websocket:
        for client in connected_clients:
            if(client.open):
                await client.send(message)    
        

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())