from http.server import SimpleHTTPRequestHandler, HTTPServer

# HTML content that the honeypot serves
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
    # Logs IP, port, and request headers
    def log_message(self, format, *args):
        client_ip, client_port = self.client_address
        print(f"IP: {client_ip} PORT: {client_port}")
        for header, value in self.headers.items():
            print(f"{header}: {value}")
    
    # Handles GET requests
    def do_GET(self):
        print("Processing GET request...")
        if self.path == "/IMG_7234.webp":  # Serve the WebP image if requested
            try:
                with open("IMG_7234.webp", "rb") as img:
                    self.send_response(200)
                    self.send_header("Content-type", "image/webp")
                    self.end_headers()
                    self.wfile.write(img.read())
                    self.wfile.flush()
                print("Served WebP image successfully.")
            except FileNotFoundError:
                print("WebP image not found.")
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
                self.wfile.flush()
        else:  # Serve the main HTML content for all other GET requests
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(HTML_CONTENT)))
            self.end_headers()
            self.wfile.write(HTML_CONTENT)
            self.wfile.flush()
            print("Served HTML content successfully.")
    
    # Handles POST requests
    def do_POST(self):
        print("Processing POST request...")
        content_length = int(self.headers.get("Content-Length", 0))  # Get data length
        post_data = self.rfile.read(content_length)  # Read the POST data
        print("Received POST data:", post_data.decode("utf-8"))  # Log data
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>POST request received</h1></body></html>")
        self.wfile.flush()
        print("Responded to POST request.")

# Define host and port
host, port = 'localhost', 8080
server = HTTPServer((host, port), HoneypotHandler)

# Start the server
print(f"Starting honeypot server at http://{host}:{port}")
server.serve_forever()