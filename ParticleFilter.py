from __future__ import absolute_import

import random
from math import *
import bisect
import time
from draw import World


landmarks  = [[50.0,50.0]]
world_size = 100.0
randomness = 200
sigma2 = 0.9 ** 2
def w_gauss(a, b):
    error = a - b
    g = e ** -(error ** 2 / (2 * sigma2))
    return g



class WeightedDistribution(object):
    def __init__(self, state):
        accum = 0.0
        self.state = [p for p in state if p.w > 0]
        self.distribution = []
        for x in self.state:
            accum += x.w
            self.distribution.append(accum)

    def pick(self):
        try:
            return self.state[bisect.bisect_left(self.distribution, random.uniform(0, 1))]
        except IndexError:
            # Happens when all particles are improbable w=0
            return None

class Particle(object):
    def __init__(self):
#        self.x = random.random() % world_size
#        self.y = random.random() % world_size      
        self.x =  random.gauss(0,0.1) 
        self.y =  random.gauss(0,0.1) 
        self.w = 1.0
        self.theta =  random.gauss(0,100)
#       self.theta = random.random() * 2.0 * pi
        
        
    def __repr__(self):
        return "(%f, %f, theta=%f)" % (self.x, self.y, self.theta)
    
    def set(self, new_x, new_y, new_orientation,w=1):
#        if new_x < 0 or new_x >= world_size:
#            raise ValueError, 'X coordinate out of bound'
#        if new_y < 0 or new_y >= world_size:
#            raise ValueError, 'Y coordinate out of bound'
#        if new_orientation < 0 or new_orientation >= 2 * pi:
#            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.theta = float(new_orientation)
        self.w  = w

    def move(self):
        self.x += cos(self.theta) 
        self.y += sin(self.theta)
        self.theta = self.theta
        if(self.x > abs(world_size / 2 )):
            self.x = -self.x
        if(self.y > abs(world_size / 2 )):
            self.y = -self.y
         
    def measurement(self):
        return   random.gauss(self.x, 0.1) 
              



if __name__ == "__main__":
    myrobot = Particle()
    print 'Robot: ',
    print myrobot
    N = 500    # Total number of particles
    T = 500

    p = []
    for i in range(N):
        r = Particle()
        p.append(r)    
    
    # Normalise weights
    nu = sum(particle.w for  particle in p)
    if nu:
        for particle in p:
            particle.w = particle.w / nu
            
    # Display world
    world = World(world_size, landmarks)
    world.draw()
    world.show_robot(myrobot)
    world.show_particles(p)
    
    for t in range(T):
        myrobot.move()
        Z = myrobot.measurement()       

        for part in p:
            part.move()
        
        for particle in p:
            particle.w  = w_gauss(Z,particle.x)
    

        # Display world
        world.show_robot(myrobot)
        world.show_particles(p)
        
        
        # create a weighted distribution, for fast picking
        dist = WeightedDistribution(p)
        
#        
#        # Normalise weights
#        nu = sum(part.w for part in p)
#        if nu:
#            for part in p:
#                part.w = part.w / nu
    

        new_particles = []
        size = len(p)
        for i,r in enumerate(p):
            pr = dist.pick()
            r = int(random.uniform(0,size+randomness))
            new_particle = Particle()
            if pr is not None:
                if r  not in range(size,size+randomness):  
                    new_particle.set(random.gauss(pr.x,0.2), random.gauss(pr.y,0.2),random.gauss(pr.theta,0.1),pr.w)
                else:
                    new_particle.set(pr.x, pr.y,pr.theta,pr.w)       
            new_particles.append(new_particle)
        p = new_particles
        #print len(p)
        time.sleep(.1)
        #raw_input()
        
        
#        
#        # Particle resampling
#        p3 = []
#        beta = 0.0
#        mw = 0.0
#        for particle in p:            
#            if particle.w > mw:
#                mw = particle.w
#        index = int(random.random() * N)
#
#        for particle in p:
#            beta +=  2.0 * mw
#            while beta > particle.w:
#                print beta,particle.w
#                beta -= particle.w
#                index = (index + 1) % N
#            p3.append(p[index])
#        time.sleep(1)
#        p = p3
    