
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from wsgiref.types import StartResponse, WSGIApplication, WSGIEnvironment
from typing import Callable, Optional

import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import asyncio
import threading
from common.router import Router
from common.server import Server
from ws.webSocketServer import WebSocketServer

import glob
import json
import base64
import cgi
from dotenv import load_dotenv
from ultralytics import YOLO, settings


load_dotenv()

app = Router()
ws = WebSocketServer()


def read_file(filepath):
    with open(filepath, 'rb') as file:
        return file.read()

def read_image_files(folder_path):
    image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff"]
    image_files = []
    for pattern in image_patterns:
        image_files.extend(glob.glob(os.path.join(folder_path, pattern)))
    return image_files

def encode_image_to_base64(filepath):
    with open(filepath, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
@app.route('/api/createImage', methods=['POST'])
def create_image(environ):
   # TODO to replace with multipart library
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)
    file_item = form['file']
    
    if file_item.filename:
        file_path = os.path.join('uploads', file_item.filename)
        with open(file_path, 'wb') as output_file:
            output_file.write(file_item.file.read())
        
        response = {"message": "Image created", "filename": file_item.filename}
        return json.dumps(response).encode('utf-8'), 'application/json; charset=utf-8'
    else:
        response = {"message": "No file uploaded"}
        return json.dumps(response).encode('utf-8'), 'application/json; charset=utf-8'

model = YOLO("yolov8n.pt")

def draw_boxes(image, results):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    for result in results:
        for *box, conf, cls in result:
            x1, y1, x2, y2 = map(int, box)
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1), f'{model.names[int(cls)]} {conf:.2f}', fill="red", font=font)
    return image

@app.route('/api/getImages')
def get_images(environ):
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'uploads')
        image_files = read_image_files(file_path)
        
        encoded_images = []

        for index, image_file in enumerate(image_files):
            image = Image.open(image_file)
            
            image_np = np.array(image)
            
            results = model(image_np, save=True )
        
            imagePath = f"{results[0].save_dir}/{results[0].path}"
            
            file_path = os.path.join(os.path.dirname(__file__), 'uploads')
            encoded_image = encode_image_to_base64(imagePath)
            
     
            
            # Add to the list of encoded images
            encoded_images.append({
                "filename": os.path.basename(image_file),
                "data": encoded_image
            })
    except Exception as inst:
        print('error', inst)
        return  json.dumps({"status": 500, "message": "fail"}).encode('utf-8'), 'application/json; charset=utf-8'

    response = {"images": encoded_images}
    return json.dumps(response).encode('utf-8'), 'application/json; charset=utf-8'
    


def cors_middleware(app: WSGIApplication):
    def middleware(environ: WSGIEnvironment, start_response: StartResponse):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', '*'))
            return start_response(status, headers, exc_info)

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            start_response('204 No Content', [('Access-Control-Allow-Origin', '*'),
                                              ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
                                              ('Access-Control-Allow-Headers', 'Content-Type')])
            return [b'']
        return app(environ, custom_start_response)
    return middleware

server = Server(app, "uploads", os.environ['PORT'], os.environ['HOST'], middleware=cors_middleware)





def start_servers():
    # Start the WSGI server
    threading.Thread(target=server.start).start()

    # Start the WebSocket server
    asyncio.run(ws.start())

if __name__ == "__main__":
    start_servers()