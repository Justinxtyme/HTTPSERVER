# IMPORT SOCKET MODULE
import socket

#CREATING SERVER
# CREATE TCP SOCKET AF_INET= IPV4 SOC_STREAM = TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#BINDING
server_address = ('localhost', 65432)
#BIND SOCKET TO SERVER ADRESS
server_socket.bind(server_address)
print(f"Server listening on {server_address}")