from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MyServer(HTTPServer):
    def __init__(self, address, request_handler):
        super().__init__(address, request_handler)


class MyRequestHandler(BaseHTTPRequestHandler):
    path_handlers: dict

    def __init__(self, request, client_address, server_class):
        self.path_handlers = {
            "/": "Welcome to root!",
            "/view": "<html><body><p>This is the view!</p><body></html>",
            "/json": {"message": "Hello World!"}
        }
        super().__init__(request, client_address, server_class)


    def do_GET(self):
        if self.path not in self.path_handlers:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("The content you are trying to access cannot be found on the server".encode('utf8'))
            return
        response = self.path_handlers[self.path]
        self.send_response(200)
        if isinstance(response, str):
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(len(response)))
        elif isinstance(response, dict):
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(json.dumps(response))))
        self.end_headers()
        self.wfile.write(str(response).encode('utf8'))
        # self.wfile.write(response.encode('utf8'))


    def add_path_handler(self, path, response_content):
        self.path_handlers[path] = response_content

def start_server(addr="127.0.0.1", port=80):
    server_address = (addr, port)
    print(server_address)
    http_server = MyServer(server_address, MyRequestHandler)
    # http_server.add_path_handler("/", "Welcome to root!")
    # http_server.add_path_handler("/view", "<html><body><p>This is the view!</p><body></html>")

    print(f"Starting server on {addr}:{port}")
    http_server.serve_forever()


def main():
    start_server()


if __name__ == '__main__':
    main()
