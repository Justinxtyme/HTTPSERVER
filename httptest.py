#IMPORT MINIMUM 
from http.server import HTTPServer, BaseHTTPRequestHandler

# SET HOST AND PORT
server_address = ('localhost', 8000) 

#CREATING SERVER INSTANCE
httpd = HTTPServer(server_address, BaseHTTPRequestHandler)

# START SERVER TO ALLOW CONNECT
httpd.startforever()

# DEFINING CUSTOM HANDLER
class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # Status code: OK
        self.send_header('Content-type', 'text/html')  # Content type: HTML
        self.end_headers()  # End headers
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")  # Response body