# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:50:47 2015

@author: Rachel
"""
import pandas 
import numpy as np
import matplotlib.pyplot as plt


def ave_ar_vs_strain(hot):
    ax = hot.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', yerr = 'std', color = 'k')    
    ax.set_xlabel('Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Average Aspect Ratio', fontsize = 20)
    ax.set_ylim([1, 5])
    fit = np.polyfit(hot['bulk_strain'], hot['AR'], 2)
    x = np.linspace(0, 1, 20) 
    y = fit[2] + (fit[1] * x) + (fit[0] * (x**2)) 
    ax.plot(x, y, 'k--')
    ax.legend(['raw',' y = {0}x^2 + {1}x + {2}'.format("{:.2f}".format(fit[0]), "{:.2f}".format(fit[1]), "{:.2f}".format(fit[2]))], 2, fontsize = 14)


def den_vs_bulk_strain(hot):
    '''
    plots the dendrite vs. bulk strain given a data frame
    
    '''
    #plt.rcParams['mathtext.default']='custom'
    
    ax = hot.plot(kind = 'scatter',  x = 'bulk_strain', y = 'den_strain', color = 'k')
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
    ax.plot(x, regY, 'k-')
    ax.plot(x, maxY, 'k--')
    
    #plots Jesi's strain data on the linear regression of my data
    ax.plot([0.20, 0.31], [regFit[0] * 0.20 + regFit[1], regFit[0] * 0.31 + regFit[1]], 'w^')
    
    ax.plot(hot['bulk_strain'], hot['den_max'], 'k.')
    ax.legend(['reference', 'strain', '1 ' + r'${\sigma}$','EBSD strain'], 2, fontsize = 16)
    ax.plot(hot['bulk_strain'], hot['den_min'], 'k.')
    ax.plot(x, minY, 'k--')
    
def main():
    hot = pandas.read_csv('bulk_den_strain_hot.csv', sep = ",", header = 0)
    room = pandas.read_csv('bulk_den_strain_rt.csv', sep = ",", header = 0)
    
    hot['den_min'] = (((hot['AR'] - hot['std']) / 1.324021) ** .5) -1
    hot['den_max'] = (((hot['AR'] + hot['std']) / 1.324021) ** .5) -1
    
    den_vs_bulk_strain(hot)
    #ave_ar_vs_strain(hot)
    