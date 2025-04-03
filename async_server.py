import asyncio
import socket

async def handle_client(client_socket):
    """Handle a single client connection."""
    loop = asyncio.get_event_loop()

    try:
        # Step 1: Read the full HTTP request from the client until headers are complete
        data = b""
        while True:
            chunk = await loop.sock_recv(client_socket, 1024)
            if not chunk:
                break
            data += chunk
            # Check for the end of headers
            if b"\r\n\r\n" in data:
                break

        # Debugging: Print raw request
        print(f"Raw request received: {data}")

        if not data:
            # Handle empty requests
            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 0\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            await loop.sock_sendall(client_socket, response.encode('utf-8'))
            print("Sent 400 Bad Request due to empty input.")
        else:
            # Step 2: Decode and verify request
            request = data.decode('utf-8', errors='replace').strip()
            print(f"Decoded request: {request}")

            # Ensure it's a valid HTTP request (should start with "GET ")
            if request.startswith("GET "):
                response_body = "Message received!"
                response_headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                full_response = response_headers + response_body
            else:
                # Handle invalid requests
                full_response = (
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 0\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

            await loop.sock_sendall(client_socket, full_response.encode('utf-8'))
            print(f"Response sent: {full_response.strip()}")

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        # Step 3: Ensure connection is properly closed
        client_socket.close()

async def main():
    # Step 1: Create a raw socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow immediate reuse of the address after the server stops.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(('localhost', 8888))  # Bind to localhost
    server_socket.listen(5)  # Queue up to 5 connections
    server_socket.setblocking(False)  # Non-blocking mode for asyncio
    print("Server listening on http://localhost:8888")

    loop = asyncio.get_event_loop()

    # Step 2: Accept client connections asynchronously
    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)
        print(f"New client connected from: {client_address}")
        asyncio.create_task(handle_client(client_socket))

# Start the server
asyncio.run(main())