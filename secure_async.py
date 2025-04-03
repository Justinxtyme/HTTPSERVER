import asyncio
import ssl

async def handle_client(reader, writer):
    """Handle a single client connection."""
    try:
        # Read request
        request = await reader.read(1024)
        if not request:
            return  # Client disconnected

        request = request.decode('utf-8')
        print(f"Request:\n{request}")

        # Determine response
        if request.startswith("GET / ") or request.startswith("GET /HTTP"):
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
            writer.write(response.encode('utf-8'))

        elif "GET /styles.css" in request:
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
            writer.write(response.encode('utf-8'))

        elif "GET /image.jpg" in request:
            try:
                with open("image.jpg", "rb") as image_file:
                    image_data = image_file.read()

                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n" + image_data)
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\nImage not found."
                writer.write(response.encode('utf-8'))

        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found."
            writer.write(response.encode('utf-8'))

        await writer.drain()  # Ensure data is sent before closing
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    server = await asyncio.start_server(handle_client, 'localhost', 8443, ssl=ssl_context)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on https://{addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()

asyncio.run(main())