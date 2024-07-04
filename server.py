
import os
from wsgiref.types import WSGIApplication


class Server:
    def __init__(self, app:WSGIApplication, uploadFolderName):
        self.app = app
        self.uploadFolderName = uploadFolderName

    def createUploadFolder(self):
         if not os.path.exists(self.uploadFolderName):
                os.makedirs(self.uploadFolderName)

    def start(self):
        if __name__ == 'server':
            self.createUploadFolder()
            from wsgiref.simple_server import make_server
            server = make_server('localhost', 8000, self.app)
            print("Serving on port 8000...")
            server.serve_forever()