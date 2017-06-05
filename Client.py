# send socket data in field like '110011100'

from socket import socket
import pygame


def get_cell_center(pos):
    return pos[0] - pos[0] % 100 + 50, pos[1] - pos[1] % 100 + 50


def cell_to_index(pos):
    x = (pos[0] - 50)/100
    y = (pos[1] - 50)/100
    return int(3 * y + x)


def index_to_cell(index):
    return (index % 3) * 100 + 50, (index // 3) * 100 + 50


def draw_empty_field():
    game_display.fill(pygame.Color("#ffffff"))
    for i in range(3):
        pygame.draw.line(game_display, BLACK, (0, i * 100), (300, i * 100))
        pygame.draw.line(game_display, BLACK, (i * 100, 0), (i * 100, 300))
    pygame.display.update()


def update_field(field):
    draw_empty_field()
    for i in range(len(field)):

        cell = index_to_cell(i)
        print(cell)
        if field[i] == 1:
            # DRAW CROSS
            pygame.draw.line(game_display, BLACK, (cell[0]-10, cell[1]-10), (cell[0]+10, cell[1]+10))
        if field[i] == 2:
            pygame.draw.circle(game_display, BLACK, cell, 20, 20)
        pygame.display.update()


BLACK = pygame.Color("#000000")
WIDTH = 300
HEIGHT = 300
WIN_SIZE = (WIDTH, HEIGHT)
pygame.init()
game_display = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("XO-game")

#GAME FIELD
game_field = [0 for i in range(9)]

# DRAW GAME FIELD
draw_empty_field()

# SOCKET CONNECTION
client_socket = socket()
client_socket.connect(('192.168.1.103', 53211))
game_state = client_socket.recv(1)
if game_state == b'f' or game_state == b's':
    player_state = input("Type 'r' when you are ready: ")
    if player_state == 'r':
        client_socket.send(b'r')

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if game_state == b'f':
            if e.type == pygame.MOUSEBUTTONDOWN:
                cell = get_cell_center(pygame.mouse.get_pos())
                index = cell_to_index(cell)
                if game_field[index] == 0:
                    game_field[index] = 1
                    update_field(game_field)
                else:
                    print('pos is checked')
                    print(game_field)
                client_socket.send(''.join(map(str, game_field)).encode())
                game_field = list(client_socket.recv(1024).decode())
                update_field(game_field)

        elif game_state == b's':
            game_field = list(client_socket.recv(1024).decode())
            update_field(game_field)
            if e.type == pygame.MOUSEBUTTONDOWN:
                cell = get_cell_center(pygame.mouse.get_pos())
                index = cell_to_index(cell)
                if game_field[index] == 0:
                    game_field[index] = 2
                    pygame.draw.circle(game_display, BLACK, cell, 20, 20)
                    pygame.display.update()
                else:
                    print('pos is checked')
                    print(game_field)
                client_socket.send(''.join(map(str, game_field)).encode())


'''
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
'''