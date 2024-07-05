
import sys
import os

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

@app.route('/api/getImages')
def get_images(environ):
    file_path = os.path.join(os.path.dirname(__file__), 'uploads')
    image_files = read_image_files(file_path)
    encoded_images = [{"filename": os.path.basename(image), "data": encode_image_to_base64(image)} for image in image_files]
    response = {"images": encoded_images}
    return json.dumps(response).encode('utf-8'), 'application/json; charset=utf-8'



server = Server(app, "uploads", os.environ['PORT'], os.environ['HOST'])

def start_servers():
    # Start the WSGI server
    threading.Thread(target=server.start).start()

    # Start the WebSocket server
    asyncio.run(ws.start())

if __name__ == "__main__":
    start_servers()

