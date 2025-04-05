from http.server import SimpleHTTPRequestHandler, HTTPServer

class HoneypotHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        client_ip, client_port = self.client_address
        print(f"IP: {client_ip} PORT: {client_port}")
        for header, value in self.headers.items():
            print(f"{header}: {value}")
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <h1>Welcome</h1>
            <a href="/sensitive-data">Sensitive Data</a>
            <form method="POST" action="/login">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
        """)

host, port = 'localhost', 8080
server = HTTPServer((host, port), HoneypotHandler)

server.serve_forever()