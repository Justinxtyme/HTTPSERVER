from http.server import SimpleHTTPRequestHandler, HTTPServer

class HoneypotHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        client_ip, client_port = self.client_address
        print(f"IP: {client_ip} PORT: {client_port}")
        for header, value in self.headers.items():
            print(f"{header}: {value}")

host, port = 'localhost', 8080
server = HTTPServer((host, port), HoneypotHandler)

server.serve_forever()