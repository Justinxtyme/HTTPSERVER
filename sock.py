# IMPORT SOCKET MODULE
import socket

#CREATING SERVER
# CREATE TCP SOCKET AF_INET= IPV4 SOC_STREAM=TCP/SOCK_DGRAM=UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#SETTING HOST AND PORT
server_address = ('localhost', 65432)

# SET TIMEOUT
s.settimeout(5)  # Timeout after 5 seconds

#BIND SOCKET TO SERVER ADRESS
server_socket.bind(server_address)
print(f"Server listening on {server_address}")

#OPEN FOR INCOMING CONNECTIONS
server_socket.listen()

#ACCEPTING CONNECTION
connection, client_address = server_socket.accept()
print(f"Connection from {client_address}")

#RECIEVE DATA FROM CLIENT
data = connection.recv(1024)  # Read up to 1024 bytes(adjustable)
print(f"Received: {data.decode('utf-8')}")
#FOR BIGGER TRANSFERS
"""
data = b""
while True:
    chunk = s.recv(1024)  # Read in chunks
    if not chunk:
        break
    data += chunk
               """
#SEND RESPONSE TO CLIENT
connection.sendall(b"Hello, Client!") 

#CLOSE IT!
connection.close()

