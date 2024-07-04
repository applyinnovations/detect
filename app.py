# myapp.py
from backend import Backend
from server import Server
import os
import glob
import json
import base64
import cgi

app = Backend()

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

@app.route('/')
def index(environ):
    html_content = read_file('index.html')
    return html_content, 'text/html; charset=utf-8'

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
    image_files = read_image_files('uploads')
    encoded_images = [{"filename": os.path.basename(image), "data": encode_image_to_base64(image)} for image in image_files]
    response = {"images": encoded_images}
    return json.dumps(response).encode('utf-8'), 'application/json; charset=utf-8'

server = Server(app, "uploads")

server.start()