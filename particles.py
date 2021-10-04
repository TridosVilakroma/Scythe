import pygame,random,time
from random import randint
from color_palette import *

class ParticleEmitter():
    def __init__(self,emit_rate,x_range,y_range,colors,size,*motion_styles):
        self.emit_rate=emit_rate
        self.emit_limit=time.time()
        self.x_range=x_range
        self.y_range=y_range
        self.colors=colors
        self.size=size
        self.motion_styles=motion_styles
        self.particles=[]

    class Particle():
        def __init__(self,pos,color,size):
            self.pos=pos
            self.color=color
            self.size=size
            self.dest=pos
            self.movement_vector=pygame.math.Vector2(0,0)
   
    def limiter(self):
        #emit_rate is time intervals between return of True booleans 
        time_stamp=time.time()
        if time_stamp>self.emit_limit:
            self.emit_limit=time_stamp+self.emit_rate
            return True
        else:
            return False

    def randomize_pos(self,x_range,y_range):
        x=randint(x_range[0],x_range[1])
        y=randint(y_range[0],y_range[1])
        return (x,y)

    def randomize_color(self,colors):
        color=random.choice(colors[0])
        return color

    def create_particle(self):
        particle=self.Particle(pygame.math.Vector2(self.randomize_pos(self.x_range,self.y_range)),
        self.randomize_color(self.colors),self.size)
        self.particles.append(particle)

    def particle_filter(self):
        particles_copy=[i for i in self.particles if i.size > 0]
        self.particles=particles_copy

    def draw_all_particles(self,screen):
        if self.particles:
            for i in self.particles:
                pygame.draw.circle(screen,i.color,i.pos,int(i.size))

    def shrink(self,size):
        size-=.005
        return size
        
    '''motion_styles is used to select as many of the following styles desired
    and apply them to the particleEmitter object on creation.
    '''

    def move_to_dest(self):
        for i in self.particles:
            if i.dest!=(0,0):
                i.movement_vector=pygame.math.Vector2(i.pos-i.dest)
                i.pos+=i.movement_vector
                i.dest=pygame.math.Vector2(0,0)


    def ascend(self):
        for i in self.particles:
            i.pos[1] += 1

    def fire_fly(self):
        for i in self.particles:
            chance=randint(1,75)
            if chance==1:
                randint_a=randint(i.pos[0]-5,i.pos[0]+5)
                randint_b=randint(i.pos[1]-5,i.pos[1]+5)
                i.dest=pygame.math.Vector2(randint_a,randint_b)




    def update(self,screen):
        if self.limiter():
            self.create_particle()
        self.fire_fly()
        self.move_to_dest()
        for particle in self.particles:
            particle.size=self.shrink(particle.size)
            for style in self.motion_styles:
                style(self)
        self.draw_all_particles(screen)