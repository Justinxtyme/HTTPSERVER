import asyncio

async def handle_client(reader, writer):
    """Handle a single client connection."""
    try:
        # Read the full HTTP request header until "\r\n\r\n" is found.
        data = b""
        while True:
            chunk = await reader.read(1024)
            if not chunk:
                break
            data += chunk
            if b"\r\n\r\n" in data:
                break

        if not data:
            writer.close()
            await writer.wait_closed()
            return

        request = data.decode('utf-8', errors='replace')
        print(f"Request:\n{request}")

        # Parse the request line (first line) for proper routing
        request_line = request.splitlines()[0] if request.splitlines() else ""

        # Route the request based on the path
        if request_line.startswith("GET /styles.css"):
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
            try:
                with open("IMG_7231.webp", "rb") as image_file:
                    image_data = image_file.read()
                writer.write(
                    b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n" + image_data
                )
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\nImage not found."
                writer.write(response.encode('utf-8'))

        elif request_line.startswith("GET /"):
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
            response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found."
            writer.write(response.encode('utf-8'))

        await writer.drain()  # Ensure data is sent before closing

    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on http://{addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()

asyncio.run(main())