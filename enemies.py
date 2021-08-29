import pygame,time
from random import randint

class Scarecrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        
        self.hp = randint(3,10)
        self.defense = randint(0,3)
        self.x=randint(0,968)
        self.y=randint(0,468)
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def vitality(self):
        if self.hp == 0:
            self.kill()
            
    def update(self):
        self.vitality()
