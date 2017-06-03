# send socket data in field like '110011100'

from socket import socket

client_socket = socket()
client_socket.connect(('192.168.1.103', 53211))
client_socket.send(b'110011100')
echo = client_socket.recv(9)
client_socket.close()
print('Recevied: ', echo)
print(type(echo))