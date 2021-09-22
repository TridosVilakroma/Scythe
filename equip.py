import pygame
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
        mana_drain=.25
        self.image=pygame.image.load(r'media\relics\mephitidae_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\mephitidae_relic.png')
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=220
        self.scythe_attack=0
        self.hp_regen=.005
    def attack(self):
        print('bite')
    def special_attack(self):
        print('cloud')
    def passives(self):
        pass

Mephitidae_relic=Skunk()

class Fox(Relic):
    def __init__(self):
        mana_drain=.35
        self.image=pygame.image.load(r'media\relics\vulpes_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\vulpes_relic.png')
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=235
        self.scythe_attack=0
        self.hp_regen=0
        
    def attack(self):
        print('arrow')
    def special_attack(self):
        print('mine')
    def passives(self):
        pass
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
        mana_drain=.15
        self.image=pygame.image.load(r'media\relics\aeetos_relic.png')
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\eagle\eagle_neutral.png')
        super().__init__(mana_drain,self.image)
        self.defense=1
        self.speed=170
        self.scythe_attack=0
        self.hp_regen=0
    def attack(self):
        print('arrow')
    def special_attack(self):
        print('mine')
    def passives(self):
        pass
        #prox=(abs(player1pos[0]-self.rect.center[0]),abs(player1pos[1]-self.rect.center[1]))
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

armor={
    
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