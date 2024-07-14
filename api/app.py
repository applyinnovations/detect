#!/usr/bin/python3.7

import base64
import os
from aiohttp import web, WSCloseCode
import asyncio
from webSocket import WebsockeHandler
from PIL import Image
import numpy as np
from ultralytics import YOLO

websocket_handler = WebsockeHandler()

async def read_image_files(file_path):
    return [os.path.join(file_path, f) for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def create_image(request):
    reader = await request.multipart()
    
    field = await reader.next()
    if field.name != 'file':
        return web.json_response({"message": "No file uploaded"})
    
    filename = field.filename
    file_path = os.path.join('uploads', filename)
    
    size = 0
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    
    response = {"message": "Image created", "filename": filename}
    return web.json_response(response)
    


async def get_images(request):
    try:
        model = YOLO("yolov8n.pt")
        file_path = os.path.join(os.path.dirname(__file__), 'uploads')
        image_files = await read_image_files(file_path)
        
        encoded_images = []

        for index, image_file in enumerate(image_files):
            image = Image.open(image_file)
            image_np = np.array(image)
            
            results = model(image_np, save=True)
            imagePath = f"{results[0].save_dir}/{results[0].path}"
            
            encoded_image = encode_image_to_base64(imagePath)
            
            # Add to the list of encoded images
            encoded_images.append({
                "filename": os.path.basename(image_file),
                "data": encoded_image
            })
    except Exception as inst:
        print('error', inst)
        return web.json_response({"status": 500, "message": "fail"}, status=500)

    response = {"images": encoded_images}
    return web.json_response(response)



def createUploadFolder(uploadFolderName):
    if not os.path.exists(uploadFolderName):
        os.makedirs(uploadFolderName)


def create_runner():
    app = web.Application()
    app.add_routes([
        web.post('/api/createImage', create_image),
        web.get('/api/getImages', get_images),
        web.get('/ws', websocket_handler.handler),
    ])
    return web.AppRunner(app)

# TODO should come from env
async def start_server(host='0.0.0.0', port=80):
    createUploadFolder('uploads')
    runner = create_runner()
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()