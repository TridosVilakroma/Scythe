from pygame.constants import JOYBUTTONDOWN,JOYBUTTONUP
import pygame,time,math,random
from pygame.sprite import collide_mask
import common_functions as comfunc
import enemies,equip,particles,boss
from color_palette import *
import controller as con
from controller import ControllerReferences as refcon
import Time

game=None#variable overwritten in main to allow blit access from this module
scyman=None#variable overwritten in main to allow blit access from this module
screen=None#variable overwritten in main to allow blit access from this module
canvas=None#variable overwritten in main to allow blit access from this module
scarecrows=None#variable overwritten in main to add enemy access here
structures=None#variable overwritten in main to add enemy access here
# attacks=[]
# enemies.attacks=attacks
# boss.attacks=attacks

class Companion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.hover_text=pygame.sprite.Group()
        self.x=1500
        self.y=750
        self.x_precise=self.x
        self.y_precise=self.y

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self,value):
        self.rect.x=value
    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self,value):
        self.rect.y=value
    @property
    def precise_rect(self):
        return (self.x_precise,self.y_precise,32,32)
    @precise_rect.setter
    def precise_rect(self,value):
        self.x_precise=value[0]
        self.y_precise=value[1]

    def collide(self):
        collision_tolerence=10
        #canvas boundaries
        if self.x_precise<32:
            self.x_precise=32
        if self.x_precise>2936:
            self.x_precise=2936
        if self.y_precise<32:
            self.y_precise=32
        if self.y_precise>1436:
            self.y_precise=1436
        #confined to player ones screen
        #right edge
        if int(game.canvas_pos[0])<=-2031:
                if self.x<2032:
                    self.x=2032
                    self.x_precise=2032
        elif self.x<scyman.x-484:
            self.x=scyman.x-484
            self.x_precise=scyman.x-484
        #left side
        if int(game.canvas_pos[0])>=31:
                if self.x>936:
                    self.x=936
                    self.x_precise=936
        elif self.x>scyman.x+484:
                self.x=scyman.x+484
                self.x_precise=scyman.x+484
        #top side
        if int(game.canvas_pos[1])>=31:
                if self.y>436:
                    self.y=436
                    self.y_precise=436
        elif self.y>scyman.y+234:
            self.y=scyman.y+234
            self.y_precise=scyman.y+234
        #bottom side
        if int(game.canvas_pos[1])<=-1031:
                if self.y<1032:
                    self.y=1032
                    self.y_precise=1032
        elif self.y<scyman.y-234:
            self.y=scyman.y-234
            self.y_precise=scyman.y-234

    def collision_check(self,xy,old_pos):
        for i in structures:
            if self.rect.colliderect(i.hit_box):
                if xy=='x':
                    self.x=old_pos
                    self.x_precise=old_pos
                elif xy=='y':
                    self.y=old_pos
                    self.y_precise=old_pos
                break
        for i in scarecrows:
            if self.rect.colliderect(i.hit_box):
                if xy=='x':
                    self.x=old_pos
                    self.x_precise=old_pos
                elif xy=='y':
                    self.y=old_pos
                    self.y_precise=old_pos
                break

    def traverse(self):
        delta=Time.delta()
        self.last_pos=self.x,self.y
        motionx=refcon.P2.get_axis(0)
        motiony=refcon.P2.get_axis(1)
        #directions=['up','right','down','left']
        angle=con.joy_angle(refcon.P2,(0,1))% 360
        up=0
        right=90
        down=180
        left=270
        if math.isclose(up, angle, abs_tol = 45):
            self.direction='up'
        if math.isclose(right, angle, abs_tol = 45):
            self.direction='right'
        if math.isclose(down, angle, abs_tol = 45):
            self.direction='down'
        if math.isclose(left, angle, abs_tol = 45):
            self.direction='left'
        if not comfunc.dead_zone(refcon.P2,(0,1)):
            # self.animate_switch()
            if not comfunc.dead_zone(refcon.P2,single_axis=0):
                old_x=self.x_precise
                if motionx>0:
                    self.x_precise+=(self.speed*delta)*refcon.P2.get_axis(0)
                    self.x=self.x_precise
                    self.collision_check('x',old_x)
                if motionx<0:
                    self.x_precise+=(self.speed*delta)*refcon.P2.get_axis(0)
                    self.x=self.x_precise
                    self.collision_check('x',old_x)
            if not comfunc.dead_zone(refcon.P2,single_axis=1):
                old_y=self.y_precise
                if motiony<0:
                    self.y_precise+=(self.speed*delta)*refcon.P2.get_axis(1)
                    self.y=self.y_precise
                    self.collision_check('y',old_y)
                if motiony>0:
                    self.y_precise+=(self.speed*delta)*refcon.P2.get_axis(1)
                    self.y=self.y_precise
                    self.collision_check('y',old_y)

    def draw(self):
        canvas.blit(self.image,(self.x,self.y))
        self.hover_text.update()
        self.hover_text.draw(canvas)

    def focus_switch(self):
        self.traverse()

    def auxillary(self):
        self.collide()

    def update(self):
        self.focus_switch()
        self.auxillary()
        self.draw()

class Mami(Companion):
    def __init__(self):
        self.image=pygame.image.load(r"media\multiplayer_icons\mami.png").convert_alpha()
        self.speed=180
        super().__init__()
        self.image_loader()

    def image_loader(self):
        self.idle_images=[]

class Shep(Companion):
    def __init__(self):
        self.image=pygame.image.load(r"media\multiplayer_icons\shep.png").convert_alpha()
        self.speed=180
        super().__init__()