import socket
import asyncio

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_adress = ("localhost", 8888)
