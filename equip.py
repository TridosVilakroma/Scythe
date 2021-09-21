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
        self.shape_shifted=pygame.image.load(r'media\relics\skunk\skunk.png')
        self.shape_shifted=pygame.transform.rotozoom(self.shape_shifted,0,.4)
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=220
        self.scythe_attack=0
        self.hp_regen=.005
    def attack(self):
        print('cloud')

Mephitidae_relic=Skunk()


egg=Skunk()
blue=Skunk()
pink=Skunk()
diamond=Skunk()
egg.image=pygame.image.load(r'media\relics\4_relic.png')
blue.image=pygame.image.load(r'media\relics\3_relic.png')
pink.image=pygame.image.load(r'media\relics\2_relic.png')
diamond.image=pygame.image.load(r'media\relics\5_relic.png')
relics={
    1:Mephitidae_relic
    }
###############ARMOR###############

armor={
    1:egg
}
###############WEAPONS###############

class Scythe(Weapon):
    def __init__(self, image, damage, cooldown):
        super().__init__(image, damage, cooldown)
        
weapons={
    1:blue
}
###############TOOLS###############

tools={
    1:pink,
    2:diamond
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