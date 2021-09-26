import pygame, sys, math,time

def quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def sprite_parser(sheet,frame,width,height,color=(0,0,0)):
    image=pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),((frame*width),0,width,height))
    image.set_colorkey(color)
    return image

def dead_zone(controller,joy_stick):
    x_axis = controller.get_axis(joy_stick[0])
    y_axis = controller.get_axis(joy_stick[1])
    if abs(x_axis) > .3 or abs(y_axis) > .3:
        return False
    else:
        return True

def move(rect_center,speed,angle):
    x = rect_center[0] + (speed*math.cos(math.radians(angle)))
    y = rect_center[1] + (speed*math.sin(math.radians(angle)))
    return x,y

def attack_collide(attack,sprite2):
    if attack.self.rect.colliderect(sprite2.rect):
        sprite2.hp-=attack.power-sprite2.defense

def clean_list(list,element):
    while True:
        try:
            list.remove(element)
        except ValueError:
            break

class ItemSprite(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image=image
        self.mask=pygame.mask.from_surface(image)
        self.rect=image.get_rect()

def item_decay(nested_list):
    '''To remove elements from a nested list based
    on life-time limits.
    Nested lists must contain object as first element, and objects
    must have a life_time attribute passed into function
    '''
    filtered_list=[]
    for i in nested_list:
        if i[0].life_time >= time.time():
            filtered_list.append(i)
    return filtered_list

def sprite_decay(group):
    '''This function will kill sprites based on
    self.life_time attributes
    '''
    filtered_group=pygame.sprite.Group()
    for i in group:
        if i.life_time >= time.time():
            filtered_group.add(i)
    return filtered_group

