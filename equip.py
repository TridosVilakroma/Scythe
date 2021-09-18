import pygame
#Base equipment class
class Equipment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()

class Relic(Equipment):
    def __init__(self,mana_drain):
        super().__init__()
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
Unique equipment will be subclassed from 
the four basic equipment sub-classes defined above

"""
###############RELICS###############

class Skunk(Relic):
    def __init__(self):
        mana_drain=1
        super().__init__(mana_drain)
        self.image=pygame.image.load(r'media\relics\relic.png')

###############ARMOR###############


###############WEAPONS###############

class Scythe(Weapon):
    def __init__(self, image, damage, cooldown):
        super().__init__(image, damage, cooldown)
        

###############TOOLS###############