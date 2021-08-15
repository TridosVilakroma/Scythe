import pygame, time, random, sys
import common_functions as comfunc
screen_width = (1000)
screen_height = (500)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Scythe')
corner_flair=pygame.image.load("media\Corner_flair.png")
joysticks = (pygame.joystick.get_count())
if joysticks >0:
    P1 = pygame.joystick.Joystick(0)
    P1.init()
    if joysticks >1:
        P2 = pygame.joystick.Joystick(1)
        P2.init()

class GameElements():
    def __init__(self):
        self.focus= 'start'

    def start_screen(self):
        vecna=pygame.font.Font("media\VecnaBold.ttf",150)
        title_text = vecna.render("Welcome",True,(222, 151, 81))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            comfunc.quit(event)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy == 0:
                   self.focus='main'
                elif event.joy == 1:
                    print('test')
        screen.fill((0, 95, 65))
        screen.blit(corner_flair,(0,467))
        screen.blit(title_text,((screen_width/2 -title_text.get_rect().width/2,screen_height/4 -title_text.get_rect().height/2)))
        pygame.display.flip()

    def main_menu(self):

        screen.fill((0, 95, 65))
        pygame.display.flip()
        print()
    
    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
game = GameElements()


while True:
    clock.tick(60)
    game.focus_switch()