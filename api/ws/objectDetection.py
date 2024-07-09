import base64


def encode_image_to_base64(filepath):
    with open(filepath, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
class ObjectDetection:
    def __init__(self, image):
        self.image = image