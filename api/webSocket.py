#!/usr/bin/env python

from aiohttp import web, WSCloseCode
import base64
import io
import os
import shutil

from PIL import Image
import aiohttp
from ultralytics import YOLO, settings

connected_clients = set()
image_name = "received_image.jpg"
runsDirectory = os.path.join(os.path.dirname(__file__), 'runs')

class WebsockeHandler:
    def __init__(self):
        self.isDetectingObject = False
    async def handler(self,request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        connected_clients.add(ws)
        print(f'Client connected: {ws}')

        try:
            async for message in ws:
                print('this is the message', message.data )
                processedImage = await self.process_image(message.data)
                await ws.send_str(processedImage)
        finally:
            connected_clients.remove(ws)
            print(f'Client disconnected: {ws}')

        return ws

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