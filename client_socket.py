import socket

# Step 1: Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect to the server
server_address = ('localhost', 65432)
client_socket.connect(server_address)

# Step 3: Send and receive data
client_socket.sendall(b"Hello, Server!")
data = client_socket.recv(1024)
print(f"Received: {data.decode('utf-8')}")

# Step 4: Close the connection
client_socket.close()