#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 17:35:42 2021

@author: moyuan
"""


import numpy as np
import itertools
import math
class Swimmer2d:
    
    def __init__(self, D, va=0, vfield=None, alpha = 0):
        self.x = 0
        self.y = 50
        self.theta = 0 #theta is the angle the orientation makes with the y axis
        self.D = D
        self.Dr = D*3
        self.va = va
        self.v0 = va
        self.dt = 0.1
        self.vfield = vfield
        self.vfx=0
        self.vfy=0
        self.alpha = alpha
        self.PTL = 10;
        if self.vfield!=None:
            self.vfx = vfield[0]
            self.vfy = vfield[1]

        self.ymin = 0
        self.xmin = -10
        self.xmax = 10
        self.Lx = 20
        self.traj = []
        self.ori = []

    
    def updateva(self):
        # self.va = max(self.v0-self.alpha*self.y, -self.vfy*2)
        self.va = 2
        if self.y <42:
            nP = np.floor(self.y/self.PTL)
            zOut = self.y- nP*self.PTL
            self.va = 10 - nP*2
            if zOut < 2:
                self.va += math.erfc(zOut)
            if zOut > 8:
                self.va -= math.erfc(self.PTL-zOut)
        if self.y <2:
            self.va = 10
        
        # self.va=10-np.floor(z*self.alpha)-math.erf
    
    def step(self):
        """
        single step method for a swimmer, encoding the thermal brownian motion,
        the active swimming.

        Returns
        -------
        None.

        """
        
        
        """ record position and orientation """
        self.traj.append([self.x, self.y])
        self.ori.append(self.theta)
        
        """ change the active speed """
        self.updateva()
        
        """ The thermal brownian motion with gaussian white noise """
        self.x += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfx)*self.dt
        self.y += (np.sqrt(2*self.D/self.dt)*np.random.normal()+self.vfy)*self.dt
        
        """ The active swimming """
        self.theta += np.sqrt(2*self.Dr/self.dt)*np.random.normal()*self.dt
        self.x += np.sin(self.theta)*self.va*self.dt
        self.y += np.cos(self.theta)*self.va*self.dt

        if self.y < self.ymin:
            self.y = self.ymin
        if self.x < self.xmin:
            self.x=self.x+self.Lx
        if self.x > self.xmax:
            self.x=self.x-self.Lx
    def time_evo(self, T_total):
        """
        Take T_total number of step using the built in step method

        Parameters
        ----------
        T_total : Integer
            The total number of time step to take.

        Returns
        -------
        None.

        """
        for i in range(T_total):
            self.step()
        # va = 
    # def getTraj(self):
    #     return self.traj
        
class ActiveEnsemble:
    ens=[]

    def __init__(self, N, D, va, vfield=None,alpha=0):
        self.D = D
        self.N=N
        # self.record_orientation = record_orientation
        
        self.ens = [Swimmer2d(D=D, va= va, vfield=vfield,alpha=alpha) for i in range(N)]
        
    
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
        density, bins = np.histogram(pos, bins=60)
        bins = bins[1:]-(bins[1]-bins[0])/2
        return [density, bins]
    
    def filterOri(self, TS= 1000, zmin = 5):
        t_total = len(self.ens[0].traj)
        o = []
        zmin_c = zmin+self.ens[0].ymin
        for w in self.ens:
            for t in range(TS, t_total):
                if w.traj[t][1]>zmin_c:
                    o.append(w.ori[t])
        
        o = np.arctan2(np.sin(o),np.cos(o))
        return o
    def filterOriZbin(self, Tsteady, zLow, zHigh):
        ori = []
        zLow = self.ens[0].ymin+zLow
        zHigh = self.ens[0].ymin+zHigh
        for w in self.ens:
            for t in range(Tsteady, len(w.traj)):
                if w.traj[t][1] > zLow and w.traj[t][1]<zHigh:
                    ori.append(w.ori[t])
        sin = [np.sin(i) for i in ori]
        cos = [np.cos(i) for i in ori]
        ori_wrapped = [np.arctan2(sin[i],cos[i]) for i in range(len(sin))]
        return ori_wrapped

    def savedata(self, filename):
        import pandas as pd
        df = pd.DataFrame({})
        for i in range(self.N):
            df['traj{0}'.format(i)]=self.ens[i].traj
        df.to_csv(filename+'traj.csv')
        df = pd.DataFrame({})
        for i in range(self.N):
            df['ori{0}'.format(i)]=self.ens[i].ori
        df.to_csv(filename+'ori.csv')
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