import socket
import pygame
import os
pygame.init()


width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Player(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self, x, y, sprite="C:\\Users\\15154\\Pictures\\Kalya\\paper.png"):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([20, 20])

        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale(self.image, (96, 105))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.fake_x = x
        self.fake_y = y

        self.off_set_x = 0
        self.off_set_y = 0


player_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

player1 = Player(300, 300, "C:\\Users\\15154\\Pictures\\Kalya\\paper.png")
player2 = Player(300, 300, "C:\\Users\\15154\\Pictures\\Kalya\\stapler.png")

all_sprites_list.add(player1)
all_sprites_list.add(player2)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((HOST, PORT))

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.fake_x -= 2
            player1.off_set_x -= 2
        if keys[pygame.K_RIGHT]:
            player1.fake_x += 2
            player1.off_set_x += 2
        if keys[pygame.K_DOWN]:
            player1.fake_y += 2
            player1.off_set_y += 2
        if keys[pygame.K_UP]:
            player1.fake_y -= 2
            player1.off_set_y -= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    exit()

        screen.fill((255, 255, 255))

        conn.sendall(bytes(str(player1.fake_x) + "," + str(player1.fake_y), 'utf-8'))
        # player1.offset_x = 0
        # player1.offset_y = 0

        data = conn.recv(1024)
        if data:
            incoming = data.decode("utf-8")
            incoming = incoming.split(",")
            player2.rect.x = int(incoming[0]) - player1.off_set_x
            player2.rect.y = int(incoming[1]) - player1.off_set_y

        if not data:
            break
        all_sprites_list.draw(screen)
        pygame.display.flip()
