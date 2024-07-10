#!/usr/bin/env python

import asyncio
import base64
import io
import os
import shutil
import cv2
from websockets import WebSocketServerProtocol
from websockets.server import serve
from PIL import Image
from ultralytics import YOLO, settings


connected_clients = set()
image_name = "received_image.jpg"
runsDirectory = os.path.join(os.path.dirname(__file__), 'runs')

class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = int(port)
        self.isDetectingObject = False

    async def handler(self, websocket:WebSocketServerProtocol):
    
        connected_clients.add(websocket)
        
        async for message in websocket:
            for client in connected_clients:
                if(client.open & self.isDetectingObject == False):
                    processedImage = await self.process_image(message)
                    await client.send(processedImage)

    async def main(self):
        async with serve(self.handler,self.host, self.port):
            await asyncio.Future()  # run forever

    async def process_image(self, image_blob):
        # Convert the image blob to a PIL Image
        image = Image.open(io.BytesIO(image_blob))
        
        # Save the image temporarily
        
        image.save(image_name)
        
        if(self.isDetectingObject):
            return self.encode_image_to_base64(image_name)
        # Perform object detection and get the base64 encoded image
        processedImageSource = self.detectObject(image_name)

        encodedImage = self.encode_image_to_base64(processedImageSource)
        
        
        shutil.rmtree(runsDirectory, ignore_errors=True)
        
        
        return encodedImage
    
    def encode_image_to_base64(self, filepath):
        with open(filepath, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def detectObject(self, originalImage):
        self.isDetectingObject = True
        settings.update({"runs_dir": runsDirectory})
        model = YOLO("yolov8n.pt")
        
        results = model(originalImage, save=True )
        
        imagePath = f"{results[0].save_dir}/{image_name}"
        self.isDetectingObject = False
        return imagePath
    
          
    def start(self):
        print('calling web sockets')
        asyncio.run(self.main())