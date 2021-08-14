import pygame, time, random, sys

SCREEN_SIZE = (1000,500)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Scythe')
while True:
    clock.tick(60)
    screen.fill((0,0,0))
    pygame.display.flip()