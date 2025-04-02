import asyncio
import socket

async def main():
    # Step 1: Create a raw socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    await asyncio.get_event_loop().sock_connect(client_socket, ('localhost', 8888))

    # Step 2: Send data to the server
    message = b"Hello, Server!"
    await asyncio.get_event_loop().sock_sendall(client_socket, message)

    # Step 3: Receive response from the server
    data = await asyncio.get_event_loop().sock_recv(client_socket, 1024)
    print(f"Received: {data.decode('utf-8')}")

    # Step 4: Close the socket
    client_socket.close()

# Run the client
asyncio.run(main())