#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 17:35:42 2021

@author: moyuan
"""


import numpy as np
import itertools
class Swimmer2d:
    
    def __init__(self, D, va=0, vfield=None, record_orientation=False):
        self.x = 0
        self.y = 0
        self.theta = 0 #theta is the angle the orientation makes with the y axis
        self.D = D
        self.Dr = D*3
        self.va = va
        self.dt = 1
        self.vfield = vfield
        self.vfx=0
        self.vfy=0
        if self.vfield!=None:
            self.vfx = vfield[0]
            self.vfy = vfield[1]

        self.ymin = -50
        self.traj=[]
        self.record_orientation = record_orientation
        self.ori = []
    def step(self):
        self.traj.append([self.x, self.y])
        
        """ The thermal brownian motion with gaussian white noise """
        self.x += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfx)*self.dt
        self.y += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfy)*self.dt
        
        """ The active swimming """
        self.theta += np.sqrt(2*self.Dr/self.dt)*np.random.vonmises()*self.dt
        self.x += np.sin(self.theta)*self.va*self.dt
        self.y += np.cos(self.theta)*self.va*self.dt
        if self.y < self.ymin:
            self.y = self.ymin
        
    def rostep(self):
        self.traj.append([self.x, self.y])
        self.ori.append(self.theta)
        """ The thermal brownian motion with gaussian white noise """
        self.x += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfx)*self.dt
        self.y += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfy)*self.dt
        
        """ The active swimming """
        self.theta += np.sqrt(2*self.Dr/self.dt)*np.random.normal()*self.dt
        self.x += np.sin(self.theta)*self.va*self.dt
        self.y += np.cos(self.theta)*self.va*self.dt
        if self.y < self.ymin:
            self.y = self.ymin
    def time_evo(self, T_total):
        if self.record_orientation:
            for i in range(T_total):
                self.rostep()
        else:
            for i in range(T_total):
                self.step()
        # va = 
    # def getTraj(self):
    #     return self.traj
        
class ActiveEnsemble:
    ens=[]

    def __init__(self, N, D, va, vfield=None, record_orientation=False):
        self.D = D
        self.N=N
        self.record_orientation = record_orientation
        self.ens = [Swimmer2d(D=D, va= va, vfield=vfield,record_orientation=self.record_orientation) for i in range(N)]
        
    
    def time_evo(self, T_total):
        for walker in self.ens:
            walker.time_evo(T_total)
    
    def MSD(self,time):
        
        MSD=[w.traj[time][0]**2+w.traj[time][1]**2 for w in self.ens]

        return np.mean(MSD)
    def sedProfile(self, Tsteady = 1000, axis = 1):
        pos=[]
        for w in self.ens:
            pos.extend([i[axis] for i in w.traj[Tsteady:]])
        # position=[]
        # for i in pos:
        #     position.extend(i)
        # pos=[]
        density, bins = np.histogram(pos, bins=30)
        bins = bins[1:]-(bins[1]-bins[0])/2
        return [density, bins]
    def oriProfile(self, Tsteady = 1000):
        ori = []
        for w in self.ens:
            ori.extend(w.theta)
class Walker2d:
    def __init__(self, D):
        self.x = 0
        self.y = 0

        self.D = D
        # self.v = v
        self.dt = 1
        self.traj = []
        
    def step(self):
        self.traj.append([self.x, self.y])
        # delta_r = np.sqrt(2*self.D/self.dt)*np.random.normal()*self.dt
        # rand_angle = np.random.rand()*np.pi*2
        self.x += np.sqrt(2*self.D/self.dt)*np.random.normal()*self.dt
        self.y += np.sqrt(2*self.D/self.dt)*np.random.normal()*self.dt
        
    def time_evo(self, T_total):
        for i in range(T_total):
            self.step()
        
class Ensemble_2d:

    ens=[]

    def __init__(self, N, D):
        self.D = D
        self.N=N
        self.ens = [Walker2d(D=D) for i in range(N)]
    
    def time_evo(self, T_total):
        for walker in self.ens:
            walker.time_evo(T_total)
    
    def MSD(self,time):
        
        MSD=[w.traj[time][0]**2+w.traj[time][1]**2 for w in self.ens]

        return np.mean(MSD)
    
    # def getD(self, T=1000):
        
    # def PDF(self, time):
    #     position = [w.traj[time] for w in self.ens]
    #     h = np.histogram(position, density = True)
    #     return h
    
    def reset(self):
        self.ens=[]
        self.ens = [Walker(self.x0,self.k) for i in range(self.N)]
class Walker_GWN:
    def __init__(self, x0, D,v=1):
        self.x = x0
        self.traj=[]
        self.D = D
        self.dt=1
    def step(self):
        self.traj.append(self.x)
        self.x += np.sqrt(2*self.D/self.dt)*np.random.normal()*self.dt
        
    def time_evo(self, T_total):
        for i in range(T_total):
            self.step()
            
class Ensemble_GWN:
    N=0
    ens=[]
    x0=0
    D=0
    def __init__(self, N, D, x0=0):
        self.D = D
        self.N=N
        self.ens = [Walker_GWN(x0=x0,D=D) for i in range(N)]
    
    def time_evo(self, T_total):
        for walker in self.ens:
            walker.time_evo(T_total)
    
    def MSD(self,time):
        
        MSD=[w.traj[time]**2 for w in self.ens]

        return np.mean(MSD)
    
    # def getD(self, T=1000):
        
    def PDF(self, time):
        position = [w.traj[time] for w in self.ens]
        h = np.histogram(position, density = True)
        return h
    
    def reset(self):
        self.ens=[]
        self.ens = [Walker(self.x0,self.k) for i in range(self.N)]

class Walker:
    # x = 0 #position
    # y = 0
    # D = 0 #The diffusion coeifficient
    # k = 0#The tumble rate, 1 is filp every step, 0 is never flip
    # Dr = 0
    # D=0
    # kT=0
    # gamma=1
    # sigma=1
    # v = 1
    # va= 15
    # direction = 1
    # orientation = 1
    # traj=[]
    def __init__(self, x0, D,v=1):
        self.x = x0
        self.traj=[]
        # self.y = y0
        # self.kT = kT
        # self.D = kT/self.gamma
        # self.Dr = self.D*(3/4)*((self.sigma/2)**2)
        # self.k = k
        self.D = D
        self.direction=np.random.choice([-1,1])
        self.v=v
    def step(self):
        # rand_angle = np.random.rand()*np.pi*2
        # dx = np.cos(rand_angle)
        # dy = np.sin(rand_angle)
        random_number = np.random.rand()
        if random_number<self.D:
            self.direction=self.direction*-1
        # if random_number<self.k:
        #     self.orientation  = self.orientation*-1
        self.x += self.v*self.direction
        # self.x += self.va*self.orientation
        # self.y += dy
    def time_evo(self, T_total):
        for i in range(T_total):
            self.traj.append(self.x)
            self.step()
            
    def reset(self):
        self.traj = []
        self.x=0
        
class Ensemble:
    N=0
    ens=[]
    x0=0
    D=0
    def __init__(self, N, D, x0=0):
        self.D = D
        self.N=N
        self.ens = [Walker(x0=x0,D=D) for i in range(N)]
    
    def time_evo(self, T_total):
        for walker in self.ens:
            walker.time_evo(T_total)
    
    def MSD(self,time):
        
        MSD=[w.traj[time]**2 for w in self.ens]

        return np.mean(MSD)
    
    # def getD(self, T=1000):
        
    def PDF(self, time):
        position = [w.traj[time] for w in self.ens]
        h = np.histogram(position, density = True)
        return h
    
    def reset(self):
        self.ens=[]
        self.ens = [Walker(self.x0,self.k) for i in range(self.N)]
# #%%
# w1 = Walker(x0=0, D=0.5)
# w2 = Walker(x0=0, D=0.5)
# #%%
# w1.time_evo(100)
# w2.time_evo(100)
# #%%
# import matplotlib.pyplot as plt
# plt.plot(w1.traj,'x')
# plt.plot(w2.traj,'.')
# #%%
# for i in range(10):
#     plt.plot(e.ens[i].traj[:100])
