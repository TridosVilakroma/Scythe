import pygame, sys, math,time
import Time
def quit(event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def sprite_parser(sheet,frame,width,height,color=(0,0,0)):
    image=pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),((frame*width),0,width,height))
    image.set_colorkey(color)
    return image

def dead_zone(controller,joy_stick=False,tolerance=.3,single_axis=False):
    if joy_stick:
        x_axis = controller.get_axis(joy_stick[0])
        y_axis = controller.get_axis(joy_stick[1])
        if abs(x_axis) > tolerance or abs(y_axis) > tolerance:
            return False
        else:
            return True
    elif single_axis is not False:
        axis = controller.get_axis(single_axis)
        if abs(axis) > tolerance:
            return False
        else:
            return True

def vector(obj1,obj2):
    """returns a normalized vector pointing from obj1 to obj2"""
    direction_vector=pygame.Vector2(obj2.rect.centerx-obj1.rect.centerx,obj2.rect.centery-obj1.rect.centery)
    try:
        return direction_vector.normalize()
    except ValueError:
        return direction_vector

def vector_from_coords(obj1_xy,obj2_xy):
    """returns a normalized vector pointing from obj1_xy to obj2_xy"""
    direction_vector=pygame.Vector2(obj2_xy[0]-obj1_xy[0],obj2_xy[1]-obj1_xy[1])
    try:
        return direction_vector.normalize()
    except ValueError:
        return direction_vector

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
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=image.get_rect()

def item_decay(nested_list):
    '''To remove elements from a nested list based
    on life-time limits.
    Nested lists must contain object as first element, and objects
    must have a life_time attribute passed into function
    '''
    filtered_list=[]
    for i in nested_list:
        if i[0].life_time >= Time.game_clock():
            filtered_list.append(i)
    return filtered_list

def sprite_decay(group):
    '''This function will kill sprites based on
    self.life_time attributes
    '''
    filtered_group=pygame.sprite.Group()
    for i in group:
        if i.life_time >= Time.game_clock():
            filtered_group.add(i)
    return filtered_group

def pivot(image,screen_pivot,image_pivot, angle):
    '''image is the Surface which has to be rotated and blit
    screen_pivot is the position of the pivot on the target Surface surf (relative to the top left of surf)
    image_pivot is position of the pivot on the image Surface (relative to the top left of image)
    angle is the angle of rotation in degrees
    '''
    image_rect = image.get_rect(topleft = (screen_pivot[0] - image_pivot[0], screen_pivot[1]-image_pivot[1]))
    offset_center_to_pivot = (pygame.math.Vector2(screen_pivot) - image_rect.center)
    rotated_offset = (offset_center_to_pivot.rotate(angle))
    rotated_image_center = (screen_pivot[0] - rotated_offset.x, screen_pivot[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle*-1)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return rotated_image, rotated_image_rect

def sine_pulse(speed,amplitude,lower_limit):
    '''speed- in most cases is a float to slow down pulse.
    amplitude- the highest float the pulse will reach.
    lower_limit- set the lowest float the pulse will reach(must be >=0)
    '''
    amplitude-=lower_limit
    t=(Time.game_clock()*speed) 
    pulse=abs(math.sin(t)*amplitude)
    pulse+=lower_limit
    return pulse

def cosine_pulse(speed,amplitude,lower_limit):
    '''speed- in most cases is a float to slow down pulse.
    amplitude- the highest float the pulse will reach.
    lower_limit- set the lowest float the pulse will reach(must be >=0)
    '''
    amplitude-=lower_limit
    t=(Time.game_clock()*speed) 
    pulse=abs(math.cos(t)*amplitude)
    pulse+=lower_limit
    return pulse

def surf_blur(surface,strength):
    '''blur effect is made by first strectching the surface
     then returning it to its initial size.
     the effect can be increased by repeating the process.
     strength expects an int to determine the number of cycles
     to run before returning the surface.
     '''
    rect=surface.get_rect()
    temp=surface
    x,y=rect[2],rect[3]
    for _ in range(strength):
                temp=pygame.transform.smoothscale(temp,(x*2,y*2))
                temp=pygame.transform.smoothscale(temp,(x,y))
    return temp

def center_image(surface,image):
    return pygame.Rect(
        surface.get_width()/2-image.get_width()/2,
        surface.get_height()/2-image.get_height()/2,
        image.get_width(),
        image.get_height())

