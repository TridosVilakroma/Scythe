import pygame, sys

def quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def sprite_parser(sheet,frame,width,height,color=(0,0,0)):
    image=pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),((frame*width),0,width,height))
    image.set_colorkey(color)
    return image

def dead_zone(controller):
    x_axis = controller.get_axis(0)
    y_axis = controller.get_axis(1)
    if abs(x_axis) > .3 or abs(y_axis) > .3:
        return False
    else:
        return True

def attack_collide(attack,sprite2):
    if attack.self.rect.colliderect(sprite2.rect):
        sprite2.hp-=attack.power-sprite2.defense