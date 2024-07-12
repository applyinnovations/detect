
# Add the parent directory of 'web' to sys.path
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from common.router import Router
from common.server import Server
import glob
import base64
from dotenv import load_dotenv


load_dotenv()
app = Router()

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
    file_path = os.path.join(os.path.dirname(__file__), 'index.html')
    html_content = read_file(file_path)
    return html_content, 'text/html; charset=utf-8'

@app.route('/sendVideo')
def index(environ):
    file_path = os.path.join(os.path.dirname(__file__), 'sendVideoStream.html')
    html_content = read_file(file_path)
    return html_content, 'text/html; charset=utf-8'

@app.route('/receiveVideo')
def index(environ):
    file_path = os.path.join(os.path.dirname(__file__), 'receieveVideoStream.html')
    html_content = read_file(file_path)
    return html_content, 'text/html; charset=utf-8'

server = Server(app, "uploads", 80, '0.0.0.0')

print(__name__)
if __name__ == "__main__":
      server.start()
    
