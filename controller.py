import pygame

pygame.joystick.init()
game=None#variable overwritten in main
class ControllerReferences:
    P1=None
    P2=None
    def rumble(controller,low_frequency, high_frequency, duration):
        if game.settings_data['rumble']:
            controller.rumble(low_frequency, high_frequency, duration)

def joy_init(controller_position):
    if (pygame.joystick.get_count()>=controller_position):
        con = pygame.joystick.Joystick(controller_position-1)
        return con
    else:
        return False

def joy_angle(controller,stick_num):
    vec=pygame.math.Vector2(controller.get_axis(stick_num[0]),
    controller.get_axis(stick_num[1]))
    radius, angle = vec.as_polar()
    adjusted_angle = (angle+90) % 360
    return adjusted_angle


class  ControllerTranslator:
    pass