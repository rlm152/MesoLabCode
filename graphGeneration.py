# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:50:47 2015

@author: Rachel
"""
import pandas 
import numpy as np
import matplotlib.pyplot as plt

def den_vs_bulk_strain(hot, room):
    '''
    plots the dendrite vs. bulk strain given a data frame
    
    '''
    
    hot['den_min'] = (((hot['AR'] - hot['std']) / 1.324021) ** .5) -1
    hot['den_max'] = (((hot['AR'] + hot['std']) / 1.324021) ** .5) -1
    ax = hot.plot(kind = 'scatter',  x = 'bulk_strain', y = 'den_strain', color = 'k', label = 'data')
    ax.set_xlabel('Bulk Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Dendrite Strain', fontsize = 20)
    ax.set_ylim([0, 1])
    ax.plot([0, 1], [0, 1], 'k:') 
    
    x = np.linspace(0, 1, 20) 
    minFit = np.polyfit(hot['bulk_strain'], hot['den_min'], 1)
    regFit = np.polyfit(hot['bulk_strain'], hot['den_strain'], 1)
    maxFit = np.polyfit(hot['bulk_strain'], hot['den_max'], 1)
    minY = minFit[0] * x + minFit[1]
    regY = regFit[0] * x + regFit[1]
    maxY = maxFit[0] * x + maxFit[1]
    ax.plot(x, minY, 'k--',label = '1 Sigma')
    ax.plot(x, regY, 'k-')
    ax.plot(x, maxY, 'k--')
    
    #plots Jesi's strain data on the linear regression of my data
    ax.plot([0.20, 0.31], [regFit[0] * 0.20 + regFit[1], regFit[0] * 0.31 + regFit[1]], 'w^', label = 'EBSD data')

    ax.plot(hot['bulk_strain'], hot['den_min'], 'k.')
    ax.plot(hot['bulk_strain'], hot['den_max'], 'k.')
    
    print(ax.get_legend_handles_labels())
    ax.legend(['reference', '1 sigma', 'strain'], 2, fontsize = 14)
    
    
def main():
    h = pandas.read_csv('bulk_den_strain_hot.csv', sep = ",", header = 0)
    r = pandas.read_csv('bulk_den_strain_rt.csv', sep = ",", header = 0)
    den_vs_bulk_strain(h, r)
    