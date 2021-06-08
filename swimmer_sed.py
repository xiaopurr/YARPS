#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 08:00:55 2021

@author: moyuan
"""

from YARPS.objects import *

#%%
Na= 1000; va = 10; 
edict = {'1': ActiveEnsemble(Na, D=0.1, va=va,vfield = [0, -1],record_orientation=True), '2': ActiveEnsemble(Na, D=0.1, va=va,vfield = [0, -2],record_orientation=True), 
         '3': ActiveEnsemble(Na, D=0.1, va=va,vfield = [0, -3],record_orientation=True), '4': ActiveEnsemble(Na, D=0.1, va=va,vfield = [0, -4],record_orientation=True), 
         '5': ActiveEnsemble(Na, D=0.1, va=va,vfield = [0, -5],record_orientation=True)}

keys = ['1','2','3','4','5']
T_tot= 4000
for key in keys:
    edict[key].time_evo(T_tot)

import matplotlib.pyplot as plt
import matplotlib as mpl
colors=['black','darkslategray','aqua','darkturquoise','paleturquoise']

T_steady = 1000
#%%
sed_profile=[]
for key in keys:
    sed_profile.append(edict[key].sedProfile(Tsteady=T_steady))

#%%
for p in sed_profile:
    p[1] = [i+50 for i in p[1]]
#%%sedimentation profile with fitting from Felix
def clambda(v0,vs,Dr):
    return ((v0**2)/(2*Dr*vs))*(1-(7/4)*((vs/v0)**2))
Dr = 0.1*3
lambda_list=[]
for vs in np.linspace(-1,-5,5):
    lambda_list.append(clambda(va,vs,Dr))

from scipy.optimize import curve_fit

plt.figure()
i=0
para = []
for p in sed_profile:
    def func(x,a):
        return a+(1/lambda_list[i])*x
    # p[1] = [i+10 for i in p[1]]
    # p[0] = [i/(Na*(T_tot-T_steady)) for i in p[0]]
    popt, povt = curve_fit(func, p[1][:15], np.log(p[0][:15]))
    plt.plot(p[1],p[0],'.', color=colors[i], label='vs/v0=-0.{0}'.format(keys[i]))
    fitx = np.linspace(p[1][0],p[1][-10],100)
    plt.plot(fitx, np.exp(popt[0])*np.exp((1/lambda_list[i])*fitx), color=colors[i])
    i+=1
    # para.append(popt[1])
plt.legend()
plt.yscale('log')
plt.xlabel('z')
plt.ylabel(r'$\mathcal{P}$')
plt.title('Probability Distribution for Sedimented Active Swimmer with Felix fit')
plt.savefig(fname='/home/moyuan/simulation/2021/060321/sed_profile_swim_felix.png',dpi=600)

#%%MSD
msdl = []
for key in keys:
    msd=[]
    for time in range(0,2000,100):
        msd.append(edict[key].MSD(time))
    msdl.append(msd)
#%%
for m in msdl:
    plt.plot(range(0,2000,100),m)
plt.grid(True)

#%% orientation polarization
key = '3'

o = []
for w in edict[key].ens:
    if w.y > -48:
        o.extend(w.ori[T_steady::10])
orix = [np.sin(i) for i in o]
oriy = [np.cos(i) for i in o]

o_wrap = [np.arctan2(oriy[i], orix[i]) for i in range(len(orix))]
h = np.histogram(o_wrap, bins=10)
#%%

plt.plot(h[1][1:],h[0],'.')

# #%% veff orientation?


# #%%orientation 2d hist
# key = '4'
# o=[]
# for w in edict[key].ens:
#     if w.y >-40:
#         o.extend(w.ori[3000:])
# #%%
# orix = [np.sin(i) for i in o]
# oriy = [np.cos(i) for i in o]
# #%%
# o_wrap = [np.arctan2(oriy[i], orix[i]) for i in range(len(orix))]
# h = np.histogram(o_wrap)
# #%%
# plt.plot(h[1][1:],h[0])
# #%%
# plt.hist2d(orix,oriy)
# #%%orientation
# for key in keys:
#     o=[]
#     for w in edict[key].ens:
#         if w.y>-49:
#             o.extend(w.ori[T_steady:])
#     h, bins = np.histogram([i % np.pi for i in o if i>=0], density = True)
    
    
#     plt.plot(bins[1:],h)
# #%%
# def f(theta,v0,vs):
#     return (1+ 2*vs*np.cos(theta)/v0+vs**2*np.cos(2*theta)/(2*v0**2))/(2*np.pi)
# for vs in [1,2,3,4,5]:
    
#     theta = np.linspace(-np.pi, np.pi, 1000)
#     plt.plot(theta, f(theta,10,vs))