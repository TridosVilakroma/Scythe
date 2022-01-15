import pygame

class TextHandler():
    def __init__(self,path,color,text,size,antialias=True):
        self.path = path
        self.color=color
        self.text=text
        self.size=size
        self.ref_size=size
        self.antialias=antialias
        self.font=pygame.font.Font(self.path,int(self.size))
        self.text_obj = self.font.render(self.text,self.antialias,self.color)
        self.rect=self.text_obj.get_rect()
        self.switch=False
        self.timer=0
    def shrink_pop(self,timer):
        if self.switch==False:
            if self.timer!=timer:
                self.size-=.1
                self.timer+=1
            else:
                self.timer=0
                self.switch=True
        else:
            if self.timer<timer:
                self.size+=.1
                self.timer+=1
            # elif self.timer<timer*1.75:###pop feature needs work###
            #     self.size+=.25
            #     self.timer+=1
            else:
                self.timer=0
                self.size=self.ref_size
                self.switch=False
        self.update()

    def update(self):
        self.font=pygame.font.Font(self.path,int(self.size))
        self.text_obj = self.font.render(self.text,self.antialias,self.color)
        