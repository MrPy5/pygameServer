import socket
import pygame
import os
pygame.init()

font = pygame.font.Font(os.path.join("res", "fonts", "C:\\Users\\15154\\Downloads\\vt323\\VT323-Regular.ttf"), 30)

width, height = 640, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Server")

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

messages = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #print('Connected by', addr)
        new_message = ""
        while True:
            sent = False
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
                    if event.key == pygame.K_RETURN:
                        conn.sendall(bytes(new_message, 'utf-8'))
                        messages.append("You: " + new_message)
                        sent = True
                        new_message = ""

                    if event.key == pygame.K_BACKSPACE:
                        new_message = new_message[:-1]
                    else:
                        new_message += event.unicode


            screen.fill((255,255,255))


            if sent == False:
                conn.sendall(bytes("(NAN)", 'utf-8'))
            data = conn.recv(1024)
            if data:
                incoming = data.decode("utf-8")
                if incoming != "(NAN)":
                    messages.append("Them: " + incoming)

            x = 30
            for message in messages:
                if message.startswith("You: "):
                    text_blit = font.render(message[4:], True, (0, 0, 255))
                else:
                    text_blit = font.render(message[5:], True, (0, 0, 0))
                text_blit.set_alpha(255)
                screen.blit(text_blit, (30, x))
                x += 40

            text_blit = font.render(new_message, True, (0, 0, 0))
            text_blit.set_alpha(255)
            screen.blit(text_blit, (30, 300))

            if not data:
                break
            pygame.display.flip()