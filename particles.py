import pygame,random,time,math
from random import randint
from color_palette import *

class ParticleEmitter():
    def __init__(self,emit_rate,x_range,y_range,colors,size,*motion_styles,square=False):
        self.square=square
        self.emit_rate=emit_rate
        self.emit_limit=time.time()
        self.x_range=x_range
        self.y_range=y_range
        self.colors=colors
        self.size=size
        self.motion_styles=[]
        for i in motion_styles:
            self.motion_styles.append(i)
        self.particles=[]
        self.explode_catalyst=True
        self.implode_catalyst=True
        self.explode_up_catalyst=True
        self.lightning_bolt_catalyst=True
        self.burst_emit20_catalyst=True
        

    class Particle():
        def __init__(self,pos,color,size):
            self.pos=pos
            self.color=color
            self.size=size
            self.dest=pos
            self.speed=.05
            self.movement_vector=pygame.math.Vector2(0,0)
            self.unique=randint(0,10)
    def limiter(self,speed):
        #emit_rate is a time interval between the return of True booleans
        time_stamp=time.time()*speed
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
        color=random.choice(colors)
        return color

    def create_particle(self):
        particle=self.Particle(pygame.math.Vector2(self.randomize_pos(self.x_range,self.y_range)),
        self.randomize_color(self.colors),self.size)
        self.particles.append(particle)

    def particle_filter(self):
        particles_copy=[i for i in self.particles if i.size > 0]
        self.particles=particles_copy

    def draw_all_particles(self,canvas):
        if self.particles:
            for i in self.particles:
                pygame.draw.circle(canvas,i.color,i.pos,int(i.size))

    def draw_all_particles_square(self,canvas):
        if self.particles:
            for i in self.particles:
                pygame.draw.rect(canvas,i.color,(i.pos,(int(i.size),int(i.size))))

        
    '''motion_styles is used in self.behavior() to select as many of the following 
    styles desired and apply them to each Particle object on update.
    '''
    def behavior(self):

        if 'fire_fly' in self.motion_styles:
            self.fire_fly()
        if 'move_to_dest' in self.motion_styles:
            self.move_to_dest()
        if 'move_to_dest_fast' in self.motion_styles:
            self.move_to_dest_fast()
        if 'shrink' in self.motion_styles:
            self.shrink()
        if 'slow_emit' in self.motion_styles:
            self.slow_emit()
        if 'ascend' in self.motion_styles:
            self.ascend()
        if 'fast_shrink' in self.motion_styles:
            self.fast_shrink()
        if 'random_growth' in self.motion_styles:
            self.random_growth()
        if 'vert_wave' in self.motion_styles:
            self.vert_wave()
        if 'horz_wave' in self.motion_styles:
            self.horz_wave()
        if 'halo_wave' in self.motion_styles:
            self.halo_wave()
        if 'fast_emit' in self.motion_styles:
            self.fast_emit()
        if 'explode' in self.motion_styles:
            self.explode()
        if 'implode' in self.motion_styles:
            self.implode()
        if 'explode_up' in self.motion_styles:
            self.explode_up()
        if 'fast_decay' in self.motion_styles:
            self.fast_decay()
        if 'lightning_bolt' in self.motion_styles:
            self.lightning_bolt()
        if 'shake' in self.motion_styles:
            self.shake()
        if 'burst_emit20' in self.motion_styles:
            self.burst_emit20()


    def shrink(self):
        for i in self.particles:
            i.size-=.005

    def fast_shrink(self):
        for i in self.particles:
            i.size-=.025
   
    def fast_decay(self):
        for i in self.particles:
            chance=randint(1,8)
            if chance==1:
                i.size=0

    def random_growth(self):
        for i in self.particles:
            chance=randint(1,75)
            if chance==1:
                growth=random.uniform(0,.1)
                i.size+=growth

    def move_to_dest(self):
        for i in self.particles:
            if i.dest!=(0,0):
                i.vector_length=pygame.math.Vector2(i.dest-i.pos)
                if i.vector_length.length() !=0:
                    i.pos+=(i.dest-i.pos)*i.speed
                else:
                    i.dest=pygame.math.Vector2(0,0) 

    def move_to_dest_fast(self):
        for i in self.particles:
            if i.dest!=(0,0):
                i.vector_length=pygame.math.Vector2(i.dest-i.pos)
                if i.vector_length.length() !=0:
                    i.pos+=(i.dest-i.pos)*i.speed*1.875
                else:
                    i.dest=pygame.math.Vector2(0,0)

    def slow_emit(self):
        if self.limiter(1):
            self.create_particle()
    
    def fast_emit(self):
        if self.limiter(2):
            self.create_particle()

    def burst_emit20(self):
        if self.burst_emit20_catalyst:
            self.burst_emit20_catalyst=False
            for i in range(20):
                self.create_particle()

    def lightning_bolt(self):
        if self.lightning_bolt_catalyst:
            self.particle_position_flag=-.01
            self.lightning_bolt_catalyst=False
            for i in range(100):
                self.particle_position_flag+=.01
                particle_pos=(pygame.Vector2(self.x_range[0],self.y_range[0]).lerp(pygame.Vector2(self.x_range[1],self.y_range[1]),
                self.particle_position_flag))

                particle=self.Particle(pygame.math.Vector2(particle_pos),
                self.randomize_color(self.colors),self.size*2)
                self.particles.append(particle)

    def ascend(self):
        for i in self.particles:
            i.pos[1] -=.5

    def fire_fly(self):
        for i in self.particles:
            chance=randint(1,175)
            if chance==1:
                randint_a=randint(int(i.pos[0]-5),int(i.pos[0]+5))
                randint_b=randint(int(i.pos[1]-5),int(i.pos[1]+5))
                i.dest=pygame.math.Vector2(randint_a,randint_b)

    def shake(self):
        for i in self.particles:
                randint_a=randint(int(i.pos[0]-5),int(i.pos[0]+5))
                randint_b=randint(int(i.pos[1]-5),int(i.pos[1]+5))
                i.dest=pygame.math.Vector2(randint_a,randint_b)

    def vert_wave(self):
        for i in self.particles:
            sine=math.sin(time.time()*7+i.unique)
            i.pos[0]+=sine/2

    def horz_wave(self):
        for i in self.particles:
            sine=math.sin(time.time()*7+i.unique)
            i.pos[1]+=sine/2   

    def halo_wave(self):
        for i in self.particles:
            sine=math.sin(time.time()*15+i.unique/2)
            cosine=math.cos(time.time()*15+i.unique/2)
            i.pos[0]+=sine/6
            i.pos[1]+=cosine/10

    def explode(self):
        if self.explode_catalyst:
            self.explode_catalyst=False
            for i in range(25):
                x_center=sum(self.x_range)/2
                y_center=sum(self.y_range)/2
                particle=self.Particle(pygame.math.Vector2(x_center,y_center),
                self.randomize_color(self.colors),self.size*2)
                self.particles.append(particle)
            for i in self.particles:
                randint_a=randint(int(i.pos[0]-50),int(i.pos[0]+50))
                randint_b=randint(int(i.pos[1]-50),int(i.pos[1]+50))
                i.dest=pygame.math.Vector2(randint_a,randint_b)

    def implode(self):
        if self.implode_catalyst:
            self.implode_catalyst=False
            for i in range(25):
                x_center=sum(self.x_range)/2
                y_center=sum(self.y_range)/2

                particle=self.Particle(pygame.math.Vector2(randint(int(x_center-30),
                int(x_center+30)),randint(int(y_center-30),int(y_center+30))),
                self.randomize_color(self.colors),self.size*2)
               
                self.particles.append(particle)
            for i in self.particles:
                i.dest=pygame.math.Vector2(x_center,y_center)

    def explode_up(self):
        if self.explode_up_catalyst:
            self.explode_up_catalyst=False
            for i in range(25):
                x_center=sum(self.x_range)/2
                y_center=sum(self.y_range)/2
                particle=self.Particle(pygame.math.Vector2(x_center,y_center),
                self.randomize_color(self.colors),self.size*2)
                self.particles.append(particle)
            for i in self.particles:
                randint_a=randint(int(i.pos[0]-20),int(i.pos[0]+20))
                randint_b=randint(int(i.pos[1]-75),int(i.pos[1]+5))
                i.dest=pygame.math.Vector2(randint_a,randint_b)


    def update(self,canvas):
        self.behavior()
        if self.square==True:
            self.draw_all_particles_square(canvas)
        else:
            self.draw_all_particles(canvas)