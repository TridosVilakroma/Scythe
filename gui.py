import pygame,text,Time
from color_palette import BLACK
import os.path

class Button(pygame.sprite.Sprite):
    def __init__(self,image,clicked_image,pos,text='None',purpose=None,sl_text=False):
        super().__init__()
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.image=image
        self.rect=image.get_rect()
        self.clicked_image=clicked_image
        self.rect.center=pos
        self.rect.y=self.pos[1]-self.image.get_height()
        self.depressed=False
        self.text=text
        self.render_text()
        self.purpose=purpose
        self.save_load_text(sl_text)

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

    def render_text(self):
        temp_text=text.TextHandler('media\VecnaBold.ttf',BLACK,self.text,35)
        self.image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]/2-temp_text.rect.height/2))
        self.clicked_image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]/2-temp_text.rect.height/2))

    def save_load_text(self,sl_text):
        if sl_text:
            if os.path.exists(rf'save_data\file{int(self.text[5])}_data'):
                temp_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'Load',20)
                self.image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]-temp_text.rect.height*1.25))
                self.clicked_image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]-temp_text.rect.height*1.25))
            else:
                temp_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'New',20)
                self.image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]-temp_text.rect.height*1.25))
                self.clicked_image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]-temp_text.rect.height*1.25))
class Label(pygame.sprite.Sprite):
    def __init__(self,image,pos,text='None',text_size=35):
        super().__init__()
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.original_image=image.copy()
        self.image=image
        self.rect=image.get_rect()
        self.rect.center=pos
        self.rect.y=self.pos[1]-self.image.get_height()
        self.depressed=False
        self.text=text
        self.text_size=text_size
        self.render_text()

    def render_text(self):
        self.image=self.original_image.copy()
        temp_text=text.TextHandler('media\VecnaBold.ttf',BLACK,self.text,self.text_size)
        self.image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]/2-temp_text.rect.height/2))

    def set_text(self,text,text_size=35):
        self.text=text
        self.text_size=text_size
        self.render_text()

    def draw(self,screen):
        screen.blit(self.image,self.rect.topleft)