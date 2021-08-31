from pygame.constants import JOYBUTTONDOWN
import pygame,time
import common_functions as comfunc
screen=None#variable overwritten in main to allow blit access from this module
scarecrows=None
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y):
        super().__init__()
        self.hp=10
        self.focus = 'traverse'
        self.animating=False
        self.direction='right'
        self.right_blocked,self.left_blocked=False,False
        self.down_blocked,self.up_blocked=False,False
        self.walkrightsprites =[]
        self.walkleftsprites =[]
        self.walkdownsprites =[]
        self.walkupsprites =[]
        self.blinkrightsprites =[]
        self.blinkleftsprites =[]
        self.blinkdownsprites=[]
        self.blinkupsprites=[]
        self.image_loader()
        self.current_sprite=0
        self.image=self.walkrightsprites[self.current_sprite]
        self.positionx=pos_x
        self.positiony=pos_y
        self.animate_speed=.09
        self.speed=180
        self.blink_distance=90
        self.blink_step_cooldown=.5
        self.blink_time_ref=time.time()
        self.scythe_angle=45
        self.scythe_time_ref=time.time()
        self.aux_state=[]
    def image_loader(self):
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk1.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk2.png'))
        self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink1.png'))
        self.blinkleftsprites.append(pygame.image.load('media\scyman_walk\\blink\leftblink2.png'))
        self.blinkdownsprites.append(pygame.image.load(r'media\scyman_walk\blink\downblink.png'))
        self.blinkupsprites.append(pygame.image.load(r'media\scyman_walk\blink\upblink.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png'))
        self.scythe=pygame.image.load(r'media\player_equip\wooden_scythe.png')
    def collide(self):
        collision_tolerence=5
        self.rect=pygame.Rect(self.positionx,self.positiony,self.image.get_width(),self.image.get_height())
        for i in scarecrows:
            if self.rect.colliderect(i):
                if abs(i.rect.left-self.rect.right)<collision_tolerence:
                    self.right_blocked=True
                if abs(i.rect.right-self.rect.left)<collision_tolerence:
                    self.left_blocked=True
                if abs(i.rect.top-self.rect.bottom)<collision_tolerence:
                    self.bottom_blocked=True
                if abs(i.rect.bottom-self.rect.top)<collision_tolerence:
                    self.top_blocked=True
    def animate_switch(self):
        self.animating=True   
    def traverse_animate(self):
        if self.direction=='right':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkrightsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkrightsprites[int(self.current_sprite)]
        if self.direction=='left':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkleftsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkleftsprites[int(self.current_sprite)]
        if self.direction=='up':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkupsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkupsprites[int(self.current_sprite)]
        if self.direction=='down':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkdownsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkdownsprites[int(self.current_sprite)]
    def blink_ghost(self):
        if self.blink_start>time.time()-.25:
            self.ghost.set_alpha(50)
            self.ghost_trail=self.image.copy()
            self.ghost_trail.set_alpha(150)
            screen.blit(self.ghost,self.ghostpos)
            screen.blit(self.ghost_trail,(((self.blink_startposx+self.positionx)/2),((self.blink_startposy+self.positiony)/2)))
        else:
            self.aux_state.remove('blink')
    def blink_animate(self,direction):
        self.ghostpos=(self.positionx,self.positiony)
        self.ghost=self.image.copy()
        self.aux_state.append('blink')
        if self.animating==True:
            if direction=='right':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkrightsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkrightsprites[int(self.current_sprite)]
            elif direction=='left':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkleftsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkleftsprites[int(self.current_sprite)]
            if direction=='down':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkdownsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkdownsprites[int(self.current_sprite)]
            if direction=='up':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkupsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkupsprites[int(self.current_sprite)]
        else:
            self.image=self.walkrightsprites[int(self.current_sprite)]
        self.blink_ghost()
    def vitality(self):
        pass    
    def traverse(self,P1,delta):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)

        if motionx>.5:
            if motiony>.5:#moving right down
                if self.positionx<968:
                    if self.positiony<468:
                        if not self.right_blocked:
                            self.positionx+=(self.speed*delta)*.75
                        if not self.bottom_blocked:
                            self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
            elif motiony<-.5:#moving right up
                if self.positionx<968:
                    if self.positiony>0:
                        if not self.right_blocked:
                            self.positionx+=(self.speed*delta)*.75
                        if not self.top_blocked:
                            self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()            
            elif self.positionx<968:#moving right
                if not self.right_blocked:
                    self.positionx+=self.speed*delta
                self.animate_switch()
            self.direction='right'
        elif motionx<-.5:
            if motiony>.5:#moving left down
                if self.positionx>0:
                    if self.positiony<468:
                        if not self.left_blocked:
                            self.positionx-=(self.speed*delta)*.75
                        if not self.bottom_blocked:
                            self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
            elif motiony<-.5:#moving left up
                if self.positionx>0:
                    if self.positiony>0:
                        if not self.left_blocked:
                            self.positionx-=(self.speed*delta)*.75
                        if not self.top_blocked:
                            self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()
            elif self.positionx>0:#moving left
                if not self.left_blocked:
                    self.positionx-=self.speed*delta
                self.animate_switch()
            self.direction='left'
        elif motiony>.5:#moving down
            if self.positiony<468:
                if not self.bottom_blocked:
                    self.positiony+=self.speed*delta
                self.animate_switch()
            self.direction='down'
        elif motiony<-.5:#moving up
            if self.positiony>0:
                if not self.top_blocked:
                    self.positiony-=self.speed*delta
                self.animate_switch()           
            self.direction='up'
        self.traverse_animate()
        self.right_blocked,self.left_blocked,self.bottom_blocked,self.top_blocked=False,False,False,False
    def blink_step(self,P1):
        self.blink_startposx=self.positionx
        self.blink_startposy=self.positiony
        self.focus='traverse'
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        self.animating=True
        if motionx>.5:
            self.blink_start=time.time()
            self.blink_animate('right')
            if motiony>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx+=self.blink_distance
        elif motionx<-.5:
            self.blink_start=time.time()
            self.blink_animate('left')
            if motiony>.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx-=self.blink_distance
        elif motiony>.5:
            self.blink_start=time.time()
            self.blink_animate('down')
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            else:
                self.positiony+=self.blink_distance
        elif motiony<-.5:
            self.blink_start=time.time()
            self.blink_animate('up')
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positiony-=self.blink_distance
    def scythe_slash(self,):
        self.aux_state.append('scythe')
        self.focus='traverse'
        self.scythe_time_ref=time.time()
    def scythe_animate(self):
        time_stamp=time.time()
        scythe=self.scythe.copy()
        scytheright=pygame.transform.rotozoom(scythe,-90,1)
        scytherightup=pygame.transform.rotozoom(scythe,-45,1)
        scytherightdown=pygame.transform.rotozoom(scythe,-135,1)
        scytheleft=pygame.transform.rotozoom(scythe,90,1)
        scytheleftup=pygame.transform.rotozoom(scythe,45,1)
        scytheleftdown=pygame.transform.rotozoom(scythe,135,1)
        scythedown=pygame.transform.rotozoom(scythe,180,1)
        scytheup=scythe.copy()
        if self.direction=='right':
            if time_stamp<self.scythe_time_ref+.2:
                screen.blit(scytheright,(self.rect.right-10,self.rect.center[1]-(scythe.get_height()/3)))
            elif time_stamp<self.scythe_time_ref+.5:
                screen.blit(scytherightup,(self.rect.right-15,self.rect.center[1]-(scythe.get_height()*.90)))
            else:
                comfunc.clean_list(self.aux_state,'scythe')
                self.scythe_time_ref=time_stamp
        elif self.direction=='left':
            if time_stamp<self.scythe_time_ref+.2:
                screen.blit(scytheleft,(self.rect.left-scythe.get_width()+5,self.rect.center[1]-(scythe.get_height()/1.75)))
            elif time_stamp<self.scythe_time_ref+.5:
                screen.blit(scytheleftdown,(self.rect.left-scythe.get_width(),self.rect.center[1]-(scythe.get_height()*.4)))
            else:
                comfunc.clean_list(self.aux_state,'scythe')
                self.scythe_time_ref=time_stamp
        elif self.direction=='down':
            if time_stamp<self.scythe_time_ref+.2:
                screen.blit(scythedown,(self.rect.center[0]-(scythe.get_width()*.6),self.rect.bottom-6))
            elif time_stamp<self.scythe_time_ref+.5:
                screen.blit(scytherightdown,(self.rect.center[0]-(scythe.get_width()*.45),self.rect.bottom-15))
            else:
                comfunc.clean_list(self.aux_state,'scythe')
                self.scythe_time_ref=time_stamp
        elif self.direction=='up':
            if time_stamp<self.scythe_time_ref+.2:
                screen.blit(scytheup,(self.rect.center[0]-(scythe.get_width()*.35),self.rect.top-scythe.get_height()+4))
            elif time_stamp<self.scythe_time_ref+.5:
                screen.blit(scytheleftup,(self.rect.center[0]-(scythe.get_width()*.9),self.rect.top-scythe.get_height()+2))
            else:
                comfunc.clean_list(self.aux_state,'scythe')
                self.scythe_time_ref=time_stamp

    def action(self,P1):
        time_stamp=time.time()
        if P1.get_button(0):
            if time_stamp>self.blink_time_ref:
                self.blink_time_ref=time_stamp+self.blink_step_cooldown
                self.focus ='blink'
        elif P1.get_button(2):
            self.focus='slash'  
    def focus_switch(self,P1,delta):
        self.traverse(P1,delta)
        if self.focus =='blink':
            self.blink_step(P1)
        elif self.focus=='slash':
            self.scythe_slash()
    def auxillary(self):
        if 'blink' in self.aux_state:
            self.blink_ghost()
        if 'scythe' in self.aux_state:
            self.scythe_animate()
        self.collide()
    def update(self,P1,delta):
        self.focus_switch(P1,delta)
        self.action(P1)
        self.auxillary()