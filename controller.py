import pygame

pygame.joystick.init()

def joy_init():
    joysticks = (pygame.joystick.get_count())
    if joysticks >0:
        P1 = pygame.joystick.Joystick(0)
        if joysticks >1:
            P2 = pygame.joystick.Joystick(1)
    try:
        return P1
    except UnboundLocalError:
        return None

def joy_angle(controller,stick_num):
    vec=pygame.math.Vector2(controller.get_axis(stick_num[0]),
    controller.get_axis(stick_num[1]))
    radius, angle = vec.as_polar()
    adjusted_angle = (angle+90) % 360
    return adjusted_angle