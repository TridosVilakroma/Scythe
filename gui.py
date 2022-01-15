import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self,image,clicked_image,pos,purpose=None):
        super().__init__()
        self.pos=pos
        self.image=image
        self.rect=image.get_rect()
        self.clicked_image=clicked_image
        self.rect.center=pos
        self.rect.y=self.pos[1]-self.image.get_height()
        self.depressed=False
        self.purpose=purpose

    def image_swap(self):
        self.image,self.clicked_image=self.clicked_image,self.image
        self.rect.y=self.pos[1]-self.image.get_height()

    def clicked(self):
        if not self.depressed:
            self.depressed=True
        else:
            self.depressed=False

    def activate(self):
        if self.purpose:
            return self.purpose