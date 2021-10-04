import pygame,time,particles
import common_functions as comfunc
import controller as con
from pygame.sprite import collide_mask, collide_rect, spritecollide
from color_palette import *

#Base equipment class
class Equipment(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.mask=pygame.mask.from_surface(image)
        self.rect=image.get_rect()

class Relic(Equipment):
    def __init__(self,mana_drain,image):
        super().__init__(image)
        self.mana_drain=mana_drain

class Armor(Equipment):
    def __init__(self,defense):
        super().__init__()
        self.defense=defense

class Weapon(Equipment):
    def __init__(self,damage,cooldown):
        super().__init__()
        self.damage=damage
        self.cooldown=cooldown

class Tool(Equipment):
    def __init__(self,function_unlock):
        super().__init__()
        self.function_unlock=function_unlock

"""
Unique equipment is further subclassed from 
the four basic equipment sub-classes defined above.
You will access individual equipment by it's double index,
e.g. equip_matrix[1=relics, 2=armor, 3=weapons, 4=tools][int here for index of 
nested dict]

"""
###############RELICS###############

class Skunk(Relic):
    def __init__(self):
        mana_drain=.13
        self.image=pygame.image.load(r'media\relics\mephitidae_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\skunk\skunk_neutral.png')
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=200
        self.scythe_attack=0
        self.hp_regen=0
        self.attack_count=0
        self.last_hit=time.time()
        self.cloud=False
        self.cloud_start=time.time()

    def attack(self,screen,hits,player):
        time_stamp=time.time()
        if time_stamp>self.last_hit+.15:
            self.attack_count+=1
            for i in hits:
                i.damage(1.75)
                player.hp+=1.75
                self.last_hit=time.time()
            if self.attack_count>=2:
                for i in hits:
                    i.bleed()
                    player.hp+=1.75
                self.attack_count=0

    def special_attack(self,screen):
        if not self.cloud_cooldown:
            self.cloud=True
            self.cloud_start=time.time()
            self.cloud_pos=pygame.Vector2(self.rect.center)
            self.cloud_cooldown=True

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player):
        if self.cloud and self.cloud_start>time.time()-3:
            pygame.draw.circle(screen,PURPLE,self.cloud_pos,85,1)
            for i in scarecrows:
                if i.pos.distance_to(self.cloud_pos)<85:
                    i.hp-=.075
                    i.health_bar_pop_up()
        else:
            self.cloud_cooldown=False
        


    def walk_right_load(self):
        return (r'media\relics\skunk\skunk_right.png')
    def walk_left_load(self):
        return (r'media\relics\skunk\skunk_left.png')
    def walk_up_load(self):
        return (r'media\relics\skunk\skunk_up.png')
    def walk_down_load(self):
        return (r'media\relics\skunk\skunk_down.png')

Mephitidae_relic=Skunk()

class Fox(Relic):
    def __init__(self):
        mana_drain=.15
        self.image=pygame.image.load(r'media\relics\vulpes_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\fox\fox_neutral.png')
        self.fox_mine=comfunc.ItemSprite(pygame.image.load(r'media\relics\fox\fox_mine.png'))
        self.fox_arrow=pygame.image.load(r'media\relics\fox\fox_arrow.png')
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=235
        self.scythe_attack=0
        self.hp_regen=0
        self.last_hit=time.time()
        self.mine_cooldown=time.time()
        self.mine=False
        self.arrows=pygame.sprite.Group()
        self.arrow_delay=time.time()
        
    def attack(self,screen,hits,player):
        time_stamp=time.time()
        if time_stamp>self.last_hit+.3:
            for i in hits:
                i.trap(3)
                i.damage(0)
                player.mp+=7.5
                self.last_hit=time.time()

    def special_attack(self,screen):
        if not self.mine_cooldown:
            self.mine=True
            self.mine_start=time.time()
            self.mine_pos=pygame.Vector2(self.rect.center)
            self.mine_cooldown=True
            self.fox_mine.rect[0]=(self.mine_pos[0]-self.fox_mine.image.get_width()/2)
            self.fox_mine.rect[1]=(self.mine_pos[1]-self.fox_mine.image.get_height()/2)

    def right_stick(self,delta,player,P1):
        origin=pygame.math.Vector2(player.rect.center)
        arrow=self.Arrow(self.fox_arrow,origin,P1)
        arrow.rect.center=origin
        arrow.velocity_x,arrow.velocity_y=pygame.math.Vector2((arrow.speed*delta)*(P1.get_axis(3)*8),
        (arrow.speed*delta)*(P1.get_axis(4)*8))
        if len(self.arrows)<30 and self.arrow_delay<time.time():
            self.arrows.add(arrow)
            self.arrow_delay=time.time()+.2

    def passives(self,screen,scarecrows,player):
        if self.mine and self.mine_start>time.time()-10:
            self.nuked=True
            screen.blit(self.fox_mine.image,(self.mine_pos[0]-self.fox_mine.image.get_width()/2,
            self.mine_pos[1]-self.fox_mine.image.get_height()/2))
            for i in pygame.sprite.spritecollide(self.fox_mine,scarecrows,False,collide_mask):
                self.mine_start=time.time()-10
                
        elif self.mine and self.mine_start>time.time()-10.5:
            pygame.draw.circle(screen,RED,self.mine_pos,45,1)
            if self.nuked==True:
                self.nuked=False
                for i in scarecrows:
                        if i.pos.distance_to(self.mine_pos)<45:
                            i.hp-=8
                            i.health_bar_pop_up()
        else:
            self.mine_cooldown=False
            self.nuked=False
            self.mine=False

        self.arrows=comfunc.sprite_decay(self.arrows)
        if self.arrows:
            hit_list=pygame.sprite.groupcollide(scarecrows,self.arrows,False,True,collide_mask)
            for i in hit_list:
                i.damage(2.75)
            for i in self.arrows:
                screen.blit(i.rotated_image,(i.rect.topleft))
                i.rect.x+=i.velocity_x
                i.rect.y+=i.velocity_y
   
    class Arrow(Equipment):
            def __init__(self, image,origin,P1):
                super().__init__(image)
                self.speed=150
                self.origin=origin
                self.image=image
                self.life_time=time.time()+2
                self.rotated_image=pygame.transform.rotozoom(self.image,con.joy_angle(P1,(3,4))*-1,1)
                self.velocity_x=0
                self.velocity_y=0

    def walk_right_load(self):
        return (r'media\relics\fox\fox_right.png')
    def walk_left_load(self):
        return (r'media\relics\fox\fox_left.png')
    def walk_up_load(self):
        return (r'media\relics\fox\fox_up.png')
    def walk_down_load(self):
        return (r'media\relics\fox\fox_down.png')

vulpes_relic=Fox()

class Eagle(Relic):
    def __init__(self):
        mana_drain=.18
        self.image=pygame.image.load(r'media\relics\aeetos_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\eagle\eagle_neutral.png')
        self.eagle_feather=pygame.image.load(r'media\relics\eagle\eagle_feather.png')
        super().__init__(mana_drain,self.image)
        self.defense=1
        self.speed=170
        self.scythe_attack=0
        self.hp_regen=0
        self.feathers=pygame.sprite.Group()
        self.feather_delay=time.time()
        self.entry_portal=self.Portal(pygame.image.load(r'media\relics\eagle\portal_0.png'),[PINK_PURPLE,PURPLE,DARK_PURPLE])
        self.exit_portal=self.Portal(pygame.image.load(r'media\relics\eagle\portal_1.png'),[GREEN,DARK_GREEN,LIGHT_GREEN])
        self.entry_portal_cooldown=time.time()
        self.entry_portal_lifetime=time.time()+30
        self.exit_portal_cooldown=time.time()
        self.exit_portal_lifetime=time.time()+30
        self.ghost_time=time.time()
        self.ghost_angle=10
        self.ghost_shrink=.9

    class Feather(Equipment):
            def __init__(self, image,origin,P1):
                super().__init__(image)
                self.speed=150
                self.origin=origin
                self.image=image
                self.life_time=time.time()+.5
                self.rotated_image=pygame.transform.rotozoom(self.image,con.joy_angle(P1,(3,4))*-1,1)
                self.velocity_x=0
                self.velocity_y=0
                
    class Portal(comfunc.ItemSprite):
        def __init__(self, image,*particle_colors):
            super().__init__(image)
            self.active=False
            self.particle_colors=particle_colors
            

    def attack(self,screen,hits,player):
        time_stamp=time.time()
        if self.entry_portal_cooldown<time_stamp:
            self.entry_portal_lifetime=time.time()+30
            self.entry_portal_cooldown=time.time()+3
            self.entry_portal.active=True
            self.entry_portal.rect.center=self.rect.center
            self.entry_portal.particles=particles.ParticleEmitter(.1,(self.rect.left,self.rect.right),
            (self.rect.top,self.rect.bottom),self.entry_portal.particle_colors,2)

    def special_attack(self,screen):
        time_stamp=time.time()
        if self.exit_portal_cooldown<time_stamp:
            self.exit_portal_lifetime=time.time()+30
            self.exit_portal_cooldown=time.time()+3
            self.exit_portal.active=True
            self.exit_portal.rect.center=self.rect.center
            self.exit_portal.particles=particles.ParticleEmitter(.1,(self.rect.left,self.rect.right),
            (self.rect.top,self.rect.bottom),self.exit_portal.particle_colors,2)

    def right_stick(self,delta,player,P1):
        origin=pygame.math.Vector2(player.rect.center)
        feather=self.Feather(self.eagle_feather,origin,P1)
        feather.rect.center=origin
        feather.velocity_x,feather.velocity_y=pygame.math.Vector2((feather.speed*delta)*(P1.get_axis(3)*3),
        (feather.speed*delta)*(P1.get_axis(4)*3))
        if len(self.feathers)<30 and self.feather_delay<time.time():
            self.feathers.add(feather)
            self.feather_delay=time.time()+.5

    def passives(self,screen,scarecrows,player):
        time_stamp=time.time()
        if self.entry_portal.active:
            if self.entry_portal_lifetime>time_stamp:
                self.entry_portal.particles.update(screen)
                self.entry_portal_transparent = self.entry_portal.image.copy()
                alpha = comfunc.sine_pulse(.6,175,50)
                if alpha<0:
                    alpha = 0
                self.entry_portal_transparent.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                screen.blit(self.entry_portal_transparent,self.entry_portal.rect)
                if self.exit_portal.active:
                    if self.entry_portal.rect.colliderect(player):
                        self.ghost_time=time.time()+1.2
                        self.ghost_angle=10
                        self.ghost_shrink=.9
                        self.ghost_image=player.image.copy()
                        player.positionx=self.exit_portal.rect.left
                        player.positiony=self.exit_portal.rect.top
                    if self.ghost_time>time_stamp:
                        ghost_alpha = comfunc.sine_pulse(1,250,128)
                        self.ghost_angle+=1
                        self.ghost_shrink-=.005
                        if ghost_alpha<0:
                            ghost_alpha = 0
                        self.ghost_image_rotated=pygame.transform.rotozoom(self.ghost_image,self.ghost_angle,self.ghost_shrink)
                        self.ghost_image_rotated.fill((255, 255, 255, ghost_alpha), None, pygame.BLEND_RGBA_MULT)
                        screen.blit(self.ghost_image_rotated,self.entry_portal.rect.topleft)

            else:
              self.entry_portal.active=False  

        if self.exit_portal.active:
            if self.exit_portal_lifetime>time_stamp:
                self.exit_portal.particles.update(screen)
                self.exit_portal_transparent = self.exit_portal.image.copy()
                alpha = comfunc.cosine_pulse(.5,175,50)
                if alpha<0:
                    alpha = 0
                self.exit_portal_transparent.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                screen.blit(self.exit_portal_transparent,self.exit_portal.rect)

            else:
              self.exit_portal.active=False

        self.feathers=comfunc.sprite_decay(self.feathers)
        if self.feathers:
            hit_list=pygame.sprite.groupcollide(scarecrows,self.feathers,False,True,collide_mask)
            for i in hit_list:
                i.damage(4.75)
            for i in self.feathers:
                screen.blit(i.rotated_image,(i.rect.topleft))
                i.rect.x+=i.velocity_x
                i.rect.y+=i.velocity_y

    def walk_right_load(self):
        return (r'media\relics\eagle\eagle_right.png')
    def walk_left_load(self):
        return (r'media\relics\eagle\eagle_left.png')
    def walk_up_load(self):
        return (r'media\relics\eagle\eagle_up.png')
    def walk_down_load(self):
        return (r'media\relics\eagle\eagle_down.png')

aeetus_relic=Eagle()

relics={
    1:Mephitidae_relic,
    2:vulpes_relic,
    3:aeetus_relic
    }
###############ARMOR###############
nacht_falcata=.5
armor={
    1:nacht_falcata
}
###############WEAPONS###############

class Scythe(Weapon):
    def __init__(self, image, damage, cooldown):
        super().__init__(image, damage, cooldown)
        
weapons={
    
}
###############TOOLS###############

tools={
    
}


##################################
equip_matrix={
    1:relics,
    2:armor,
    3:weapons,
    4:tools
}

#Adding all equip into a sprite group
equip=[]
for equip_types in equip_matrix.values():
    for equipment in equip_types.values():
        try:
            equip.append(equipment)
        except:
            print(Exception)