# receives a string like '100110011' which equal to
# 100
# 110
# 011 game field

from socket import socket
import time

server_socket = socket()
server_socket.bind(('192.168.1.103', 53211))
server_socket.listen(2)


while True:
    # Connection cycle
    client_first_sock, client_first_addr = server_socket.accept()
    print('Connected by :', client_first_addr)
    client_second_sock, client_second_addr = server_socket.accept()
    print('Connected by :', client_second_addr)

    print("Players are connected!")
    client_first_sock.send(b'f')
    client_second_sock.send(b's')

    while True:
        # Waiting for players ready
        first_ready = client_first_sock.recv(1)
        second_ready = client_second_sock.recv(1)
        if first_ready == b'r' and second_ready == b'r':
            print('Players are ready! ')
            break

    while True:
        # Game cycle
        first_field = client_first_sock.recv(1024)
        client_second_sock.send(first_field)
        time.sleep(3)
        second_field = client_second_sock.recv(1024)
        client_first_sock.send(second_field)
        time.sleep(3)

        if not first_field or not second_field:
            break

    client_first_sock.close()
    client_second_sock.close()
