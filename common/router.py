
from wsgiref.types import StartResponse


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=['GET']):
        def wrapper(handler):
            
            self.routes[path] = {'handler': handler, 'methods': methods}
            return handler
        return wrapper
    
    

    def __call__(self, environ, start_response:StartResponse):
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')
        route_info = self.routes.get(path)
        print("path",path)
        print("method", method)
        if route_info and method in route_info['methods']:
            response_body, content_type = route_info['handler'](environ)
            status = '200 OK'
            headers = [('Content-type', content_type)]
        else:
            response_body = b"404 Not Found"
            status = '404 Not Found'
            headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)
        return [response_body]