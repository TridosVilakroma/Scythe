import pygame

def quit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

def sprite_parser(sheet,frame,width,height,color):
    image=pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),((frame*width),0,width,height))
    image.set_colorkey(color)
    return image

def dead_zone(controller):
    x_axis = controller.get_axis(0)
    y_axis = controller.get_axis(1)
    if abs(x_axis) > .5 or abs(y_axis) > .5:
        return False
    else:
        return True