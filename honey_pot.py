from http.server import SimpleHTTPRequestHandler, HTTPServer

class HoneypotHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        client_ip, client_port = self.client_address
        user_agent = self.headers.get('User-Agent')
        print(f"IP: {client_ip}, Port: {client_port}, User-Agent: {user_agent}, Request: {self.command} {self.path}")

host, port = 'localhost', 8080
server = HTTPServer((host, port), HoneypotHandler)

server.serve_forever()
