import pygame,text,Time
from color_palette import BLACK
import os.path
from text import draw_text
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
    def __init__(self,image,pos,text='None',text_size=35,wrapping=False):
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
        self.wrapping=wrapping
        self.font=pygame.font.Font('media\VecnaBold.ttf',self.text_size)
        self.render_mode()

    def render_mode(self):
        if self.wrapping:
            self.render_wrapping_text()
        else:
            self.render_text()

    def render_text(self):
        self.image=self.original_image.copy()
        temp_text=text.TextHandler('media\VecnaBold.ttf',BLACK,self.text,self.text_size)
        self.image.blit(temp_text.text_obj,(self.rect[2]/2-temp_text.rect.width/2,self.rect[3]/2-temp_text.rect.height/2))

    def render_wrapping_text(self):
        self.image=self.original_image.copy()
        draw_text(self.image,self.text,BLACK,self.font)

    def set_text(self,text,text_size=35):
        self.text=text
        self.text_size=text_size
        self.render_mode()

    def set_image(self,image,pos):
        self.image=self.original_image.copy()
        self.image.blit(image,pos)

    def add_image(self,image,pos):
        self.image.blit(image,pos)

    def set_clipping_image(self,image,pos,clip_rect):
        surf=pygame.Surface((clip_rect[2],clip_rect[3]),pygame.SRCALPHA)
        offset=pygame.Vector2(pos)-pygame.Vector2((clip_rect[0],clip_rect[1]))
        surf.blit(image,offset)
        self.image=self.original_image.copy()
        self.image.blit(surf,clip_rect)

    def draw(self,screen):
        screen.blit(self.image,self.rect.topleft)

class ScrollY(pygame.sprite.Sprite):
    '''content needs to be a list of tuples;

    tuples must contain (color,size,*Label_text,*label_size,*(image,image_pos))

    *optional

    colors: blue,beige,brown,grey

    size: header,body'''
    def __init__(self,pos,width,content=None):
        if content is None:
            raise ValueError ('gui.Scroll() content empty')
        super().__init__()
        self.rect=pygame.Rect(pos,(width,0))
        self.content=content
        self.build_content()
        self.render_content()

    def build_content(self):
        blue_header=pygame.image.load(r'media\gui\main_menu\buttonLong_blue_pressed.png').convert_alpha()
        beige_header=pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha()
        brown_header=pygame.image.load(r'media\gui\main_menu\buttonLong_brown_pressed.png').convert_alpha()
        grey_header=pygame.image.load(r'media\gui\main_menu\buttonLong_grey_pressed.png').convert_alpha()

        blue_body=pygame.image.load(r'media\gui\main_menu\panelInset_blue.png').convert_alpha()
        beige_body=pygame.image.load(r'media\gui\main_menu\panelInset_beige.png').convert_alpha()
        brown_body=pygame.image.load(r'media\gui\main_menu\panelInset_brown.png').convert_alpha()
        grey_body=pygame.image.load(r'media\gui\main_menu\panelInset_grey.png').convert_alpha()

        for index,i in enumerate(self.content):
            type_label=i[1]
            text=i[2] if len(i)>2 else 'None'
            text_size=i[3] if len(i)>3 else 35
            sprite,sprite_pos=(i[4]) if len(i)>4 else (None,None)
            image=eval(f'{i[0]}_{i[1]}')
            image=pygame.transform.scale(image, (int(self.rect.width*.8),image.get_height()))
            if type_label=='body':
                content=Label(image,(0,0),text,text_size,wrapping=True)
            else:
                content=Label(image,(0,0),text,text_size)
            if sprite is not None:
                content.add_image(sprite,sprite_pos)
            self.content[index]=content

    def render_content(self):
        top_padding=15
        height=top_padding
        padding=5
        for i in self.content:
            i.rect=i.image.get_rect()
            height+=i.rect.height+padding
        self.surface=pygame.Surface((int(self.rect.width),int(height)), pygame.SRCALPHA)
        for index,i in enumerate(self.content):
            x=int(self.rect.width/2-i.rect.width/2)
            y=top_padding
            for item in self.content[0:index]:
                y+=item.rect.height+padding
            self.surface.blit(i.image,(x,y))

    def draw(self,screen):
        screen.blit(self.surface,self.rect.topleft)
