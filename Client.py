# send socket data in field like '110011100'

from socket import socket
import time
client_socket = socket()
client_socket.connect(('192.168.1.103', 53211))
game_state = client_socket.recv(1)
if game_state == b'f' or game_state == b's':
    player_state = input("Type 'r' when you are ready: ")
    if player_state == 'r':
        client_socket.send(b'r')
    while True:
        print(game_state)
        if game_state == b'f':
            client_socket.send(b'first player move')
            move = client_socket.recv(1024)
        else:
            move = client_socket.recv(1024)
            client_socket.send(b'second player move')
        time.sleep(3)
        if not move:
            break
    client_socket.close()
