from http.server import SimpleHTTPRequestHandler, HTTPServer

HTML_CONTENT = b"""
<html>
<body>
    <h1>Welcome</h1>
    <a href="/sensitive-data">Sensitive Data</a>
    <img src="/IMG_7234.webp" alt="Suspicious Image" width="500">
    <form method="POST" action="/login">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

class HoneypotHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        client_ip, client_port = self.client_address
        print(f"IP: {client_ip} PORT: {client_port}")
        for header, value in self.headers.items():
            print(f"{header}: {value}")
    
    def do_GET(self):
        print("Processing GET request...")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(HTML_CONTENT)))
        self.end_headers()
        self.wfile.write(HTML_CONTENT)
        self.wfile.flush()
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        print("Received POST data:", post_data.decode("utf-8"))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>POST request received</h1></body></html>")
        self.wfile.flush()

host, port = 'localhost', 8080
server = HTTPServer((host, port), HoneypotHandler)
print(f"Starting honeypot server at http://{host}:{port}")
server.serve_forever()