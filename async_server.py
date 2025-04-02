import asyncio
import socket

async def handle_client(client_socket):
    """Handle a single client connection."""
    loop = asyncio.get_event_loop()
    while True:
        try:
            # Step 1: Read data from client
            data = await loop.sock_recv(client_socket, 1024)  # Async socket recv
            if not data:
                break  # Client disconnected
            print(f"Received: {data.decode('utf-8')}")
            
            # Step 2: Send response
            await loop.sock_sendall(client_socket, b"Message received!")  # Async socket send
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()  # Close the connection

async def main():
    # Step 1: Create a raw socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)  # Queue up to 5 connections
    server_socket.setblocking(False)  # Non-blocking mode for asyncio
    print("Server listening on localhost:8888")

    # Step 2: Accept connections asynchronously
    loop = asyncio.get_event_loop()
    while True:
        client_socket, _ = await loop.sock_accept(server_socket)  # Async accept
        print("New client connected!")
        asyncio.create_task(handle_client(client_socket))  # Handle client in a coroutine

# Start the server
asyncio.run(main())