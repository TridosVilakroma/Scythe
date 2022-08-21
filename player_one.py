from pygame.constants import JOYBUTTONDOWN,JOYBUTTONUP
import pygame,time,math
from pygame.sprite import collide_mask
import common_functions as comfunc
import enemies,equip,particles
from color_palette import *
import controller as con
import Time

game=None#variable overwritten in main to allow blit access from this module
screen=None#variable overwritten in main to allow blit access from this module
canvas=None#variable overwritten in main to allow blit access from this module
scarecrows=None#variable overwritten in main to add enemy access here
structures=None#variable overwritten in main to add enemy access here
attacks=[]
enemies.attacks=attacks
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y):
        super().__init__()
        self.list_init()
        self.hp=100
        self.dead=False
        self.dying=False
        self.hp_ratio=960/self.hp
        self.mini_hp_ratio=32/self.hp
        self.hp_regen=0
        self.hp_drain_length=100
        self.drain_ratio=960/self.hp_drain_length
        self.recieved_damage=False
        self.invulnerable=False
        self.hpbar_ref_timer=Time.game_clock()
        self.hit_flash=Time.game_clock()
        self.mp=100
        self.mp_ratio=960/self.mp
        self.defense=0
        self.shield=1  #percent of damage allowed through   1==100%
        self.incoming_damage_tracked=False
        self.incoming_damage=[]
        self.focus = 'traverse'
        self.animating=False
        self.direction='right'
        self.right_blocked,self.left_blocked=False,False
        self.down_blocked,self.up_blocked=False,False
        self.image_loader()
        self.current_sprite=0
        self.image=self.walkrightsprites[self.current_sprite]
        self.rect=pygame.Rect(pos_x,pos_y,self.image.get_width(),self.image.get_height())
        self.animate_speed=.09
        self.speed=180
        self.blink_distance=90
        self.blink_step_cooldown=.5
        self.blink_mp_cost=0
        self.blink_time_ref=Time.game_clock()
        self.blink_start=Time.game_clock()
        self.scythe_angle=45
        self.scythe_time_ref=Time.game_clock()
        self.slash_time_ref=Time.game_clock()
        self.slash_cooldown=.8
        self.scythe_attack=2
        self.scythe_attack_flag=[0,0]
        self.mask=pygame.mask.from_surface(self.image)
        self.relic_cool_down=Time.game_clock()
        self.active_relic=equip.FakeRelic()
        self.scythe=self.Scythe(self.scythe_image,self.rect.center)
        self.hitlag=False
        self.x_precise=self.x
        self.y_precise=self.y
        self.rect_ratio=pygame.sprite.collide_rect_ratio(.65)
        self.lb_up=False

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

    class Scythe(equip.Equipment):
        def __init__(self, image,origin):
            super().__init__(image)
            self.speed=150
            self.origin=origin
            self.image=image
            self.original_image=image
            self.life_time=Time.game_clock()+2
            self.rotated_image=image
            self.velocity_x=0
            self.velocity_y=0

    def image_loader(self):
        self.d_pad=pygame.image.load(r'media\gui\dpad\dpad_neutral.png').convert_alpha()
        self.d_pad_up=pygame.image.load(r'media\gui\dpad\dpad_up.png').convert_alpha()
        self.d_pad_up_right=pygame.image.load(r'media\gui\dpad\dpad_upright.png').convert_alpha()
        self.d_pad_right=pygame.image.load(r'media\gui\dpad\dpad_right.png').convert_alpha()
        self.d_pad_down_right=pygame.image.load(r'media\gui\dpad\dpad_downright.png').convert_alpha()
        self.d_pad_down=pygame.image.load(r'media\gui\dpad\dpad_down.png').convert_alpha()
        self.d_pad_down_left=pygame.image.load(r'media\gui\dpad\dpad_downleft.png').convert_alpha()
        self.d_pad_left=pygame.image.load(r'media\gui\dpad\dpad_left.png').convert_alpha()
        self.d_pad_up_left=pygame.image.load(r'media\gui\dpad\dpad_upleft.png').convert_alpha()
        self.walkrightsprites.append(pygame.image.load(r'media\scyman_walk\scymanwalk0.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load(r'media\scyman_walk\scymanwalk1.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load(r'media\scyman_walk\scymanwalk2.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load(r'media\scyman_walk\scymanwalk3.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load(r'media\scyman_walk\left_walk\left_walk0.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load(r'media\scyman_walk\left_walk\left_walk1.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load(r'media\scyman_walk\left_walk\left_walk0.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load(r'media\scyman_walk\left_walk\left_walk2.png').convert_alpha())
        self.blinkrightsprites.append(pygame.image.load(r'media\scyman_walk\\blink\\rightblink1.png').convert_alpha())
        self.blinkleftsprites.append(pygame.image.load(r'media\scyman_walk\\blink\leftblink2.png').convert_alpha())
        self.blinkdownsprites.append(pygame.image.load(r'media\scyman_walk\blink\downblink.png').convert_alpha())
        self.blinkupsprites.append(pygame.image.load(r'media\scyman_walk\blink\upblink.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png').convert_alpha())
        self.walkrightsprites_white.append(pygame.image.load(r'media\scyman_walk\right_white\scymanwalk0_white.png').convert_alpha())
        self.walkrightsprites_white.append(pygame.image.load(r'media\scyman_walk\right_white\scymanwalk1_white.png').convert_alpha())
        self.walkrightsprites_white.append(pygame.image.load(r'media\scyman_walk\right_white\scymanwalk2_white.png').convert_alpha())
        self.walkrightsprites_white.append(pygame.image.load(r'media\scyman_walk\right_white\scymanwalk3_white.png').convert_alpha())
        self.walkleftsprites_white.append(pygame.image.load(r'media\scyman_walk\left_white\left_walk0_white.png').convert_alpha())
        self.walkleftsprites_white.append(pygame.image.load(r'media\scyman_walk\left_white\left_walk1_white.png').convert_alpha())
        self.walkleftsprites_white.append(pygame.image.load(r'media\scyman_walk\left_white\left_walk0_white.png').convert_alpha())
        self.walkleftsprites_white.append(pygame.image.load(r'media\scyman_walk\left_white\left_walk2_white.png').convert_alpha())
        self.walkupsprites_white.append(pygame.image.load(r'media\scyman_walk\up_white\upwalk0_white.png').convert_alpha())
        self.walkupsprites_white.append(pygame.image.load(r'media\scyman_walk\up_white\upwalk1_white.png').convert_alpha())
        self.walkupsprites_white.append(pygame.image.load(r'media\scyman_walk\up_white\upwalk0_white.png').convert_alpha())
        self.walkupsprites_white.append(pygame.image.load(r'media\scyman_walk\up_white\upwalk2_white.png').convert_alpha())
        self.walkdownsprites_white.append(pygame.image.load(r'media\scyman_walk\down_white\walkdown0_white.png').convert_alpha())
        self.walkdownsprites_white.append(pygame.image.load(r'media\scyman_walk\down_white\walkdown1_white.png').convert_alpha())
        self.walkdownsprites_white.append(pygame.image.load(r'media\scyman_walk\down_white\walkdown2_white.png').convert_alpha())
        self.walkdownsprites_white.append(pygame.image.load(r'media\scyman_walk\down_white\walkdown3_white.png').convert_alpha())
        self.scythe_image=pygame.image.load(r'media\player_equip\wooden_scythe.png').convert_alpha()
        self.scytheright=pygame.transform.rotozoom(self.scythe_image,-90,1)
        self.scytherightup=pygame.transform.rotozoom(self.scythe_image,-45,1)
        self.scytherightdown=pygame.transform.rotozoom(self.scythe_image,-135,1)
        self.scytheleft=pygame.transform.rotozoom(self.scythe_image,90,1)
        self.scytheleftup=pygame.transform.rotozoom(self.scythe_image,45,1)
        self.scytheleftdown=pygame.transform.rotozoom(self.scythe_image,135,1)
        self.scythedown=pygame.transform.rotozoom(self.scythe_image,180,1)
        self.scytheup=self.scythe_image.copy()
        self.mask_scytheright=pygame.mask.from_surface(self.scytheright)
        self.mask_scytherightup=pygame.mask.from_surface(self.scytherightup)
        self.mask_scytherightdown=pygame.mask.from_surface(self.scytherightdown)
        self.mask_scytheleft=pygame.mask.from_surface(self.scytheleft)
        self.mask_scytheleftup=pygame.mask.from_surface(self.scytheleftup)
        self.mask_scytheleftdown=pygame.mask.from_surface(self.scytheleftdown)
        self.mask_scythedown=pygame.mask.from_surface(self.scythedown)
        self.mask_scytheup=pygame.mask.from_surface(self.scytheup)

    def list_init(self):
        self.interactables=[]
        self.picked_up_items=[]
        self.relics=[equip.Testudinidae_relic,equip.Felidae_relic,equip.Panthera_relic,equip.vulpes_relic,equip.aeetus_relic]#,equip.Mephitidae_relic,equip.Ursidae_relic,
       # equip.Panthera_relic
        self.armor=[]
        self.weapons=[]
        self.tools=[]
        self.aux_state=[]
        self.enemies_hit=[]
        self.walkrightsprites =[]
        self.walkleftsprites =[]
        self.walkdownsprites =[]
        self.walkupsprites =[]
        self.walkrightsprites_white =[]
        self.walkleftsprites_white =[]
        self.walkdownsprites_white =[]
        self.walkupsprites_white =[]
        self.blinkrightsprites =[]
        self.blinkleftsprites =[]
        self.blinkdownsprites=[]
        self.blinkupsprites=[]

    def interact(self):
        for event in game.events:
            if event.type == JOYBUTTONDOWN:
                if event.__dict__['button']==3:
                    closest=None
                    if self.interactables:
                        closest=min([i for i in self.interactables],key=lambda i:i.vecpos.distance_to((self.x,self.y)))
                    if closest:
                        self.picked_up_items.append(closest)
                        self.interactables[0].kill()
                        self.item_sorter()

    def item_sorter(self):
        for i in self.picked_up_items:
            if isinstance(i,equip.Relic):
                self.relics.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Armor):
                self.armor.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Weapon):
                self.weapons.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Tool):
                self.tools.append(i)
                self.picked_up_items.remove(i)

    def collide(self):
        collision_tolerence=10
        #screen boundaries
        if self.x_precise<32:
            self.x_precise=32
        if self.x_precise>2936:
            self.x_precise=2936
        if self.y_precise<32:
            self.y_precise=32
        if self.y_precise>1436:
            self.y_precise=1436
        #collision between player and equipment
        self.interactables.clear()
        for i in pygame.sprite.spritecollide(self,enemies.spawned_loot,False):
            self.interactables.append(i)

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

    def animate_switch(self):
        self.animating=True   

    def traverse_animate(self):
        right_sprite_set=self.walkrightsprites if self.hit_flash<Time.game_clock() else self.walkrightsprites_white
        down_sprite_set=self.walkdownsprites if self.hit_flash<Time.game_clock() else self.walkdownsprites_white
        left_sprite_set=self.walkleftsprites if self.hit_flash<Time.game_clock() else self.walkleftsprites_white
        up_sprite_set=self.walkupsprites if self.hit_flash<Time.game_clock() else self.walkupsprites_white
        if self.direction=='right':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                self.animating=False
            if int(self.current_sprite)>=len(right_sprite_set):
                self.current_sprite=0
            self.image=right_sprite_set[int(self.current_sprite)]
        if self.direction=='left':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                self.animating=False
            if int(self.current_sprite)>=len(left_sprite_set):
                self.current_sprite=0
            self.image=left_sprite_set[int(self.current_sprite)]
        if self.direction=='up':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                self.animating=False
            if int(self.current_sprite)>=len(up_sprite_set):
                self.current_sprite=0
            self.image=up_sprite_set[int(self.current_sprite)]
        if self.direction=='down':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                self.animating=False
            if int(self.current_sprite)>=len(down_sprite_set):
                self.current_sprite=0
            self.image=down_sprite_set[int(self.current_sprite)]

    def blink_ghost(self):
        if self.blink_start>Time.game_clock()-.25:
            self.ghost.set_alpha(50)
            self.ghost_trail=self.image.copy()
            self.ghost_trail.set_alpha(150)
            canvas.blit(self.ghost,self.ghostpos)
            canvas.blit(self.ghost_trail,(((self.blink_startposx+self.x)/2),((self.blink_startposy+self.y)/2)))
        else:
            self.aux_state.remove('blink')

    def blink_animate(self,direction):
        self.ghostpos=(self.x,self.y)
        self.ghost=self.image.copy()
        self.aux_state.append('blink')
        if self.animating==True:
            if direction=='right':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkrightsprites):
                    self.current_sprite=0
                    self.animating=False
            elif direction=='left':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkleftsprites):
                    self.current_sprite=0
                    self.animating=False
            if direction=='down':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkdownsprites):
                    self.current_sprite=0
                    self.animating=False
            if direction=='up':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkupsprites):
                    self.current_sprite=0
                    self.animating=False
        self.blink_ghost()

    def health_bar(self):
        if self.hp>100:
            self.hp=100
        if self.hp<100:
            self.hp+=self.hp_regen
        if self.recieved_damage:
            self.hp_drain_length=self.hp_before_damage
            self.recieved_damage=False
        if self.hp_drain_length>self.hp:
            self.hp_drain_length-=.15
        drain=pygame.Rect(20,480,self.hp_drain_length*self.drain_ratio,3)
        outline=pygame.Rect(19,479,962,5)
        health=pygame.Rect(20,480,self.hp*self.hp_ratio,3)
        missing_health=pygame.Rect(20,480,960,3)
        pygame.draw.rect(screen,WHITE,outline,0,1)
        pygame.draw.rect(screen,DARK_RED,missing_health,0,1)
        pygame.draw.rect(screen,RED,drain,0,1)
        pygame.draw.rect(screen,GREEN,health,0,1)

    def mini_health_bar(self):
        time_stamp=Time.game_clock()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.mini_hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(canvas,WHITE,outline,0,1)
            pygame.draw.rect(canvas,RED,missing_health,0,1)
            pygame.draw.rect(canvas,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')

    def mana_bar(self):
        mana_regen=.1
        if self.mp>100:
            self.mp=100
        if self.mp < 100:
            self.mp+=mana_regen
        outline=pygame.Rect(19,473,962,5)
        mana=pygame.Rect(20,474,self.mp*self.mp_ratio,3)
        missing_mana=pygame.Rect(20,474,960,3)
        pygame.draw.rect(screen,WHITE,outline,0,1)
        pygame.draw.rect(screen,PURPLE,missing_mana,0,1)
        pygame.draw.rect(screen,BABY_BLUE,mana,0,1)

    def damage(self):
        for i in attacks:
            if i[1].colliderect(self.rect):
                self.hit_flash=Time.game_clock()+.1
                self.aux_state.append('health')
                self.hpbar_ref_timer=Time.game_clock()+3
                if self.incoming_damage_tracked:
                    self.incoming_damage.append(i[0])
                self.hp_before_damage=self.hp
                self.hp-=max(0,((i[0]-self.defense)*self.shield))
                self.hp_lost=abs(self.hp_before_damage-self.hp)
                self.recieved_damage=True
                self.hp=self.hp if self.hp>0 else 0
            comfunc.clean_list(attacks,i)

    def death_animation(self,screen,game):
        if not self.dying:
            self.dying=True
            game.focus='gameover'
            self.time_of_death=Time.game_clock()
            self.hit_flash=Time.game_clock()+.3
            self.death_particles=[]
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [DARK_RED,DEEP_RED,RED],
                1,
                'explode','move_out_fast'))
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [PALE_YELLOW,WORN_YELLOW,BRIGHT_YELLOW,BROWN],
                1,
                'explode','move_out_fast'))
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [RED,DARK_LEATHER,LEATHER,BROWN],
                1,
                'halo_wave','burst_emit200','move_out_fast','explode_dest'))
        if self.time_of_death>Time.game_clock()-.3:
            screen.fill(BLACK)
            radius=450+(self.time_of_death-Time.game_clock())*1400
            pygame.draw.circle(screen,WHITE,(pygame.Vector2(game.canvas_pos)+pygame.Vector2(self.rect.center)),radius,1)
            screen.blit(self.image,(pygame.Vector2(game.canvas_pos)+pygame.Vector2(self.x,self.y)))
        else:
            for i in self.death_particles:
                i.update(canvas)
            screen.blit(canvas,(game.canvas_movement()))
            if Time.game_clock()-self.time_of_death>1.4:
                self.dead=True

    def traverse(self,P1,delta):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        #directions=['up','right','down','left']
        angle=con.joy_angle(P1,(0,1))% 360
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
        if not comfunc.dead_zone(P1,(0,1)):
            self.animate_switch()
            #self.traverse_animate()
            if not comfunc.dead_zone(P1,single_axis=0):
                old_x=self.x_precise
                if motionx>0:
                    self.x_precise+=(self.speed*delta)*P1.get_axis(0)
                    self.x=self.x_precise
                    self.collision_check('x',old_x)
                if motionx<0:
                    self.x_precise+=(self.speed*delta)*P1.get_axis(0)
                    self.x=self.x_precise
                    self.collision_check('x',old_x)
            if not comfunc.dead_zone(P1,single_axis=1):
                old_y=self.y_precise
                if motiony<0:
                    self.y_precise+=(self.speed*delta)*P1.get_axis(1)
                    self.y=self.y_precise
                    self.collision_check('y',old_y)
                if motiony>0:
                    self.y_precise+=(self.speed*delta)*P1.get_axis(1)
                    self.y=self.y_precise
                    self.collision_check('y',old_y)
        self.right_blocked,self.left_blocked,self.down_blocked,self.up_blocked=False,False,False,False

    def blink_step(self,P1):
        self.blink_startposx=self.x
        self.blink_startposy=self.y
        self.focus='traverse'
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        self.animating=True
        old_x=self.x_precise
        old_y=self.y_precise
        if motionx>.5:
            self.blink_start=Time.game_clock()
            self.blink_animate('right')
            if motiony>.5:
                self.x_precise+=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise+=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            elif motiony<-.5:
                self.x_precise+=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise-=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            else:
                self.x_precise+=self.blink_distance
                self.x=self.x_precise
                self.collision_check('x',old_x)
        elif motionx<-.5:
            self.blink_start=Time.game_clock()
            self.blink_animate('left')
            if motiony>.5:
                self.x_precise-=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise+=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            elif motiony<-.5:
                self.x_precise-=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise-=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            else:
                self.x_precise-=self.blink_distance
                self.x=self.x_precise
                self.collision_check('x',old_x)
        elif motiony>.5:
            self.blink_start=Time.game_clock()
            self.blink_animate('down')
            if motionx>.5:
                self.x_precise+=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise+=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            elif motionx<-.5:
                self.x_precise-=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise+=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            else:
                self.y_precise+=self.blink_distance
                self.y=self.y_precise
                self.collision_check('y',old_y)
        elif motiony<-.5:
            self.blink_start=Time.game_clock()
            self.blink_animate('up')
            if motionx>.5:
                self.x_precise+=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise-=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            elif motionx<-.5:
                self.x_precise-=self.blink_distance/2
                self.x=self.x_precise
                self.collision_check('x',old_x)
                self.y_precise-=self.blink_distance/2
                self.y=self.y_precise
                self.collision_check('y',old_y)
            else:
                self.y_precise-=self.blink_distance
                self.y=self.y_precise
                self.collision_check('y',old_y)

    def scythe_slash(self,P1):
        self.aux_state.append('scythe')
        self.focus='traverse'
        self.scythe_time_ref=Time.game_clock()

    def scythe_animate(self,P1):
        time_stamp=Time.game_clock()

        if time_stamp<self.scythe_time_ref+.2:
            scythe,position=comfunc.pivot(self.scythe.original_image,self.rect.center,
            (16,42),con.joy_angle(P1,(0,1)))
            self.scythe.image=scythe
            self.scythe.rect=position
            self.scythe.mask=pygame.mask.from_surface(scythe)
            canvas.blit(self.scythe.image,self.scythe.rect)
            hit_list=pygame.sprite.spritecollide(self.scythe,scarecrows,False,collide_mask)
            if hit_list:
                self.hitlag=True

            if self.scythe_attack_flag[0]==0:
                self.scythe_attack_flag[0]=1
                for i in hit_list:
                    i.damage(self.scythe_attack)
        elif time_stamp<self.scythe_time_ref+.5:
            if 'scythe_twist' not in self.aux_state:
                self.aux_state.append('scythe_twist')
                self.scythe_radius=0
            self.scythe_radius+=20
            scythe,position=comfunc.pivot(self.scythe.original_image,self.rect.center,
            (16,42),con.joy_angle(P1,(0,1))-self.scythe_radius)
            self.scythe.image=scythe
            self.scythe.rect=position
            self.scythe.mask=pygame.mask.from_surface(scythe)
            canvas.blit(self.scythe.image,self.scythe.rect)
            hit_list=pygame.sprite.spritecollide(self.scythe,scarecrows,False,collide_mask)
            if hit_list:
                self.hitlag=True
            if self.scythe_radius==100 or 180 or 280:
                self.scythe_attack_flag[1]=0
            if self.scythe_attack_flag[1]==0:
                self.scythe_attack_flag[1]=1
                for i in hit_list:
                    i.damage(self.scythe_attack*3)
        else:
                comfunc.clean_list(self.aux_state,'scythe')
                comfunc.clean_list(self.aux_state,'scythe_twist')
                self.scythe_time_ref=time_stamp
                self.scythe_attack_flag=[0,0]

    def relic_select(self,P1):
        if 'dpad' not in self.aux_state:
            self.aux_state.append('dpad')
            self.dpad_timestamp=Time.game_clock()+.5
        elif self.dpad_timestamp>Time.game_clock():
            relic=self.relics
            try:
                canvas.blit(relic[0].transparent,(self.x-self.relics[0].rect[2],
                self.y))#left
            except IndexError:
                pass
            try:
                canvas.blit(relic[1].transparent,(self.x,
                self.y-self.relics[0].rect[3]))#up
            except IndexError:
                pass
            try:
                canvas.blit(relic[2].transparent,(self.x+32,
                self.y))#right
            except IndexError:
                pass
            try:
                canvas.blit(relic[3].transparent,(self.x,
                self.y+32))#down
            except IndexError:
                pass
            try:
                canvas.blit(relic[4].transparent,(self.x-self.relics[0].rect[2],
                self.y-self.relics[0].rect[3]))#upleft
            except IndexError:
                pass
            try:
                canvas.blit(relic[5].transparent,(self.x+32,
                self.y-self.relics[5].rect[3]))#upright
            except IndexError:
                pass
            try:
                canvas.blit(relic[7].transparent,(self.x-self.relics[0].rect[2],
                self.y+32))#downleft
            except IndexError:
                pass
            try:
                canvas.blit(relic[6].transparent,(self.x+32,
                self.y+32))#downright
            except IndexError:
                pass
        ##########controls##########
            cool_down=.75
            if P1.get_hat(0) == (0,0):
                canvas.blit(self.d_pad,self.rect.topleft)#neutral dpad
            elif P1.get_hat(0) == (0,1):
                canvas.blit(self.d_pad_up,self.rect.topleft)
                try:
                    canvas.blit(relic[1].image,(self.x,
                    self.y-self.relics[0].rect[3]))#up
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(1)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,1):
                canvas.blit(self.d_pad_up_right,self.rect.topleft)
                try:
                    canvas.blit(relic[5].image,(self.x+32,
                    self.y-self.relics[5].rect[3]))#upright
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(5)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,0):
                canvas.blit(self.d_pad_right,self.rect.topleft)
                try:
                    canvas.blit(relic[2].image,(self.x+32,
                    self.y))#right
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(2)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,-1):
                canvas.blit(self.d_pad_down_right,self.rect.topleft)
                try:
                    canvas.blit(relic[6].image,(self.x+32,
                    self.y+32))#downright
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(6)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (0,-1):
                canvas.blit(self.d_pad_down,self.rect.topleft)
                try:
                    canvas.blit(relic[3].image,(self.x,
                    self.y+32))#down
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(3)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,-1):
                canvas.blit(self.d_pad_down_left,self.rect.topleft)
                try:
                    canvas.blit(relic[7].image,(self.x-self.relics[0].rect[2],
                    self.y+32))#downleft
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(7)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,0):
                canvas.blit(self.d_pad_left,self.rect.topleft)
                try:
                    canvas.blit(relic[0].image,(self.x-self.relics[0].rect[2],
                    self.y))
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(0)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,1):
                canvas.blit(self.d_pad_up_left,self.rect.topleft)
                try:
                    canvas.blit(relic[4].image,(self.x-self.relics[0].rect[2],
                    self.y-self.relics[0].rect[3]))#upleft
                    if self.lb_up==True:
                        self.lb_up=False
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=Time.game_clock()+cool_down
                        self.stat_archive()
                        self.activate_relic(4)
                except IndexError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'dpad')

    def activate_relic(self,relic_index):
        relic=self.relics[relic_index]
        self.active_relic=relic
        self.activated_relic=relic_index
        self.defense=relic.defense
        self.speed=relic.speed
        self.scythe_attack=relic.scythe_attack
        self.hp_regen=relic.hp_regen
        self.attack=relic.attack

        self.walkrightsprites.clear()
        self.walkleftsprites.clear()
        self.walkupsprites.clear()
        self.walkdownsprites.clear()
        self.current_sprite=0
        self.image=relic.shape_shifted
        self.walkrightsprites.append(pygame.image.load(relic.walk_right_load()).convert_alpha())
        self.walkleftsprites.append(pygame.image.load(relic.walk_left_load()).convert_alpha())
        self.walkupsprites.append(pygame.image.load(relic.walk_up_load()).convert_alpha())
        self.walkdownsprites.append(pygame.image.load(relic.walk_down_load()).convert_alpha())

    def relic_effects(self,delta,relic_index,P1):
        relic=self.relics[relic_index]
        relic.rect.center=self.rect.center
        self.mp-=relic.mana_drain
        if P1.get_button(2):
            hits=pygame.sprite.spritecollide(self,scarecrows,False,collided=pygame.sprite.collide_rect_ratio(1.15))
            if hits:
                self.hitlag=True
            relic.attack(canvas,hits,self,P1)
        if P1.get_button(1):
            relic.special_attack(canvas,self)

        if not comfunc.dead_zone(P1,(3,4)):
            relic.right_stick(delta,self,P1)

        if self.mp<-5:
            self.mp=0
            self.deactivate_relic()
        elif self.mp<1:
            self.mp-=.5

    def stat_archive(self):
        self.defense_archive=self.defense
        self.speed_archive=self.speed
        self.scythe_attack_archive=self.scythe_attack
        self.hp_regen_archive=self.hp_regen

    def deactivate_relic(self):
        self.defense=self.defense_archive
        self.speed=self.speed_archive
        self.scythe_attack=self.scythe_attack_archive
        self.hp_regen=self.hp_regen_archive
        self.active_relic=equip.FakeRelic()
        comfunc.clean_list(self.aux_state,'relic')
        self.walkrightsprites.clear()
        self.walkleftsprites.clear()
        self.walkupsprites.clear()
        self.walkdownsprites.clear()
        self.current_sprite=0

        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png').convert_alpha())
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk1.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png').convert_alpha())
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk2.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png').convert_alpha())
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png').convert_alpha())
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png').convert_alpha())
        self.image=self.walkdownsprites[0]

    def action(self,P1):
        self.lb_up=False
        time_stamp=Time.game_clock()
        if P1.get_button(4):
            if 'relic' not in self.aux_state:
                if time_stamp>self.relic_cool_down:
                    self.dpad_timestamp=Time.game_clock()+.5
                    self.relic_select(P1)
        for event in game.events:
            comfunc.quit(event)
            if event.type == JOYBUTTONDOWN:
                if event.__dict__['button']==0:
                    if time_stamp>self.blink_time_ref:
                        if self.mp>=self.blink_mp_cost:
                            self.mp-=self.blink_mp_cost
                            self.blink_time_ref=time_stamp+self.blink_step_cooldown
                            self.focus ='blink'
                if event.__dict__['button']==2 and 'relic' not in self.aux_state:
                        if time_stamp>self.slash_time_ref:
                            self.slash_time_ref=time_stamp+self.slash_cooldown
                            self.focus='slash'
                if event.__dict__['button']==3:
                    self.interact()
                if event.__dict__['button']==4:
                    if 'relic' in self.aux_state:
                        if time_stamp>self.relic_activation_cool_down:
                            self.deactivate_relic()
                            self.relic_cool_down=Time.game_clock()+.5
                if P1.get_hat(0)[0] or P1.get_hat(0)[1]:
                    if 'relic' in self.aux_state:
                        pass
                    else:
                        if time_stamp>self.relic_cool_down:
                            self.dpad_timestamp=Time.game_clock()+.5
                            self.relic_select(P1)
            elif event.type == JOYBUTTONUP:
                if event.__dict__['button']==0:
                    pass
                if event.__dict__['button']==1:
                    pass
                if event.__dict__['button']==2:
                    pass
                if event.__dict__['button']==3:
                    pass
                if event.__dict__['button']==4:
                    if 'relic' not in self.aux_state:
                        if time_stamp>self.relic_cool_down:
                            self.lb_up=True
                            self.dpad_timestamp=Time.game_clock()+.5
                            self.relic_select(P1)

    def draw(self):
        canvas.blit(self.image,(self.x,self.y))

    def focus_switch(self,P1,delta):
        self.traverse(P1,delta)

        if self.focus =='blink':
            self.blink_step(P1)
        elif self.focus=='slash':
            self.scythe_slash(P1)

    def auxillary(self,P1,delta):
        if 'health' in self.aux_state:
            self.mini_health_bar()
        if 'blink' in self.aux_state:
            self.blink_ghost()
        if 'scythe' in self.aux_state:
            self.scythe_animate(P1)
        if 'relic' in self.aux_state:
            self.relic_effects(delta,self.activated_relic,P1)
        if not self.invulnerable:
            self.damage()
        else:
            for i in attacks:
                comfunc.clean_list(attacks,i)
        for i in self.relics:
            i.passives(canvas,scarecrows,self,P1)
        self.draw()
        if 'dpad' in self.aux_state:
            self.relic_select(P1)
        self.collide()
        self.traverse_animate()

    def update_gui(self,screen,game):
        if self.hp<=0:
            self.death_animation(screen,game)
        self.health_bar()
        self.mana_bar()

    def update(self,P1,delta):
        if self.hp<=0:
            self.traverse_animate()
            self.draw()
        else:
            self.last_pos=self.x,self.y
            self.focus_switch(P1,delta)
            self.action(P1)
            self.auxillary(P1,delta)