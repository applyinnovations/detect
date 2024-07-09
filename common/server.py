
from collections.abc import Callable
import os
import sys
from typing import Optional
from wsgiref.types import WSGIApplication
from wsgiref.simple_server import make_server

class Server:
    def __init__(self, app: WSGIApplication, uploadFolderName: str, port: int, host: str, middleware: Optional[Callable[[WSGIApplication], WSGIApplication]] = None):
        self.app = middleware(app) if middleware else app
        self.uploadFolderName = uploadFolderName
        self.port = port
        self.host = host

    def createUploadFolder(self):
         if not os.path.exists(self.uploadFolderName):
                os.makedirs(self.uploadFolderName)

    def start(self):
        self.createUploadFolder()

        if (not self.port):
             sys.exit()
        
        server = make_server('0.0.0.0', int(self.port), self.app)
        print(f"Serving http://{self.host}:{self.port}")
        server.serve_forever()