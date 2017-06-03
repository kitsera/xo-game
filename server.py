# receives a string like '100110011' which equal to
# 100
# 110
# 011 game field

from socket import socket

server_socket = socket()
server_socket.bind(('192.168.1.103', 53211))
server_socket.listen(2)

client_socket, client_addr = server_socket.accept()

while True:
    field = client_socket.recv(9)
    print("Received field: ", field)
    if not field:
        break
    client_socket.send(field)

