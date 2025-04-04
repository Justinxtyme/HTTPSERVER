import asyncio

async def handle_client(reader, writer):
    """Handle a single client connection.
    
    This function reads the full HTTP request header from the client until it
    detects the end-of-header marker ("\r\n\r\n"). It then parses the first
    line of the request to determine which file or content to serve.
    """
    try:
        # Step 1: Read the full HTTP request header until the header terminator is found.
        data = b""
        while True:
            chunk = await reader.read(1024)  # Read up to 1024 bytes at a time
            if not chunk:
                break  # No more data; client disconnected
            data += chunk
            if b"\r\n\r\n" in data:  # End of headers found
                break

        # If no data was received, close the connection.
        if not data:
            writer.close()
            await writer.wait_closed()
            return

        # Step 2: Decode the received bytes to a UTF-8 string.
        request = data.decode('utf-8', errors='replace')
        print(f"Request:\n{request}")

        # Step 3: Parse the request line (the first line of the HTTP request) for routing.
        request_line = request.splitlines()[0] if request.splitlines() else ""
        
        # Step 4: Route the request based on the path.
        if request_line.startswith("GET /styles.css"):
            # Serve the CSS file.
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
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/css\r\n"
                "\r\n" + css_content
            )
            writer.write(response.encode('utf-8'))

        elif request_line.startswith("GET /image.jpg"):
            # Serve the image. Note: Although the requested path is /image.jpg,
            # we are serving a file named "IMG_7231.webp" with the correct content type.
            try:
                with open("IMG_7231.webp", "rb") as image_file:
                    image_data = image_file.read()
                # Use "image/webp" as the content type for a WebP image.
                writer.write(
                    b"HTTP/1.1 200 OK\r\nContent-Type: image/webp\r\n\r\n" + image_data
                )
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\nImage not found."
                writer.write(response.encode('utf-8'))

        elif request_line.startswith("GET /"):
            # Serve the HTML page for the root request.
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Asyncio HTTP Server</title>
                <link rel="stylesheet" type="text/css" href="styles.css">
            </head>
            <body>
                <h1>Welcome to My Asyncio HTTP Server!</h1>
                <p>This server is running without SSL.</p>
                <img src="image.jpg" alt="Sample Image" style="display:block; margin:auto; width:50%;">
            </body>
            </html>
            """
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "\r\n" + html_content
            )
            writer.write(response.encode('utf-8'))

        else:
            # If the request doesn't match any of the above, return a 404.
            response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found."
            writer.write(response.encode('utf-8'))

        # Step 5: Ensure all data is sent out before closing the connection.
        await writer.drain()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Step 6: Close the writer to clean up the connection.
        writer.close()
        await writer.wait_closed()

async def main():
    """Start the asyncio server on localhost at port 8888 (HTTP)."""
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on http://{addr[0]}:{addr[1]}")

    # Run the server indefinitely.
    async with server:
        await server.serve_forever()

# Start the server using asyncio's event loop.
asyncio.run(main())