import pygame

def quit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
