import pygame
#Base equipment class
class Equipment(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image=image
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()

class Relic(Equipment):
    def __init__(self,image,mana_drain):
        super().__init__(image)
        self.mana_drain=mana_drain

class Armor(Equipment):
    def __init__(self,image,defense):
        super().__init__(image)
        self.defense=defense

class Weapon(Equipment):
    def __init__(self,image,damage,cooldown):
        super().__init__(image)
        self.damage=damage
        self.cooldown=cooldown

class Tool(Equipment):
    def __init__(self,image,function_unlock):
        super().__init__(image)
        self.function_unlock=function_unlock

"""
Unique equipment will be subclassed from 
the four basic equipment sub-classes defined above

"""
###############RELICS###############


###############ARMOR###############


###############WEAPONS###############

class Scythe(Weapon):
    def __init__(self, image, damage, cooldown):
        super().__init__(image, damage, cooldown)
        

###############TOOLS###############