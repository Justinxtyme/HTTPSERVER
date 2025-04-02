import asyncio
import socket
import ssl

async def handle_client(client_socket):
    """Handle a single client connection."""
    loop = asyncio.get_event_loop()
    try:
        # Step 1: Read client's HTTP request asynchronously
        request = await loop.sock_recv(client_socket, 1024)
        if not request:
            client_socket.close()
            return  # Client disconnected

        request = request.decode('utf-8')
        print(f"Request:\n{request}")

        # Step 2: Check the request path and serve appropriate content
        if "GET / " in request:
            # Serve HTML page
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Secure Asyncio HTTP Server</title>
                <link rel="stylesheet" type="text/css" href="styles.css">
            </head>
            <body>
                <h1>Welcome to My Secure Asyncio HTTP Server!</h1>
                <p>This server is now SSL encrypted!</p>
                <img src="image.jpg" alt="Sample Image" style="display:block; margin:auto; width:50%;">
            </body>
            </html>
            """
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
            await loop.sock_sendall(client_socket, response.encode('utf-8'))

        elif "GET /styles.css" in request:
            # Serve CSS file
            css_content = """
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f0f0;
            }
            h1 {
                color: darkblue;
                text-align: center;
            }
            img {
                border: 2px solid #333;
            }
            """
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{css_content}"
            await loop.sock_sendall(client_socket, response.encode('utf-8'))

        elif "GET /image.jpg" in request:
            # Serve image file
            try:
                with open("image.jpg", "rb") as image_file:
                    image_data = image_file.read()

                response = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n" + image_data
                await loop.sock_sendall(client_socket, response)
            except FileNotFoundError:
                # Handle missing image file
                response = "HTTP/1.1 404 Not Found\r\n\r\nImage not found."
                await loop.sock_sendall(client_socket, response.encode('utf-8'))

        else:
            # Default response for unknown paths
            response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found."
            await loop.sock_sendall(client_socket, response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Step 3: Close the client connection
        client_socket.close()

async def main():
    # Step 1: Create a raw socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))  # Use port 8443 for HTTPS
    server_socket.listen(5)  # Queue up to 5 connections
    server_socket.setblocking(False)  # Non-blocking mode for asyncio
    print("Server listening on https://localhost:8443")

    # Step 2: Wrap the socket with SSL
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    server_socket = ssl_context.wrap_socket(server_socket, server_side=True, do_handshake_on_connect=False)

    loop = asyncio.get_event_loop()

    # Step 3: Accept client connections asynchronously
    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)
        print(f"New client connected: {client_address}")
        asyncio.create_task(handle_client(client_socket))  # Handle client in a coroutine

# Start the server
asyncio.run(main())