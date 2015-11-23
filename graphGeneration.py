# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 12:50:47 2015

@author: Rachel
"""
import pandas 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy as sp
import sklearn.linear_model as lm

def ave_ar_vs_strain(hot):
    
    ax = hot.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', yerr = 'std', color = 'k', grid = 'off')    
    ax.set_xlabel('Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Average Aspect Ratio', fontsize = 20)
    ax.set_ylim([1, 5])
        
    x = np.linspace(-1, 1, 20) 
    offset = 1.324021
    model = pandas.ols(y = hot['AR'], x = hot['bulk_strain'], intercept = False)
    hot['fit'] = model.y_fitted    
    hot['AR_with_offset'] = hot['AR'] - offset
    model_offset = pandas.ols(y = hot['AR_with_offset'], x = hot['bulk_strain'], intercept = False)
    print(model_offset)

    y = 1.8728 * x + offset
    
    ax.plot(x, y, 'k--')
    ax.legend(['raw',' y = 1.8728 x + 1.3240, Adj R-squared = 0.9489'], 2, fontsize = 14)


def den_vs_bulk_strain(hot):
    '''
    plots the dendrite vs. bulk strain given a data frame
    
    '''
 
    ax = hot.plot(kind = 'scatter',  x = 'bulk_strain', y = 'den_strain', color = 'k', grid = 'off')
    ax.set_xlabel('Bulk Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Dendrite Strain', fontsize = 20)
    ax.set_ylim([0, 1])
    ax.plot([0, 1], [0, 1], 'k:')

    x = np.linspace(0, 1, 20)
    
    model_no_intercept = pandas.ols(y = hot['den_strain'], x = hot['bulk_strain'], intercept = False)
    print(model_no_intercept)
    hot['fit'] = model_no_intercept.y_fitted
    #ax.plot(hot['bulk_strain'], hot['fit'], 'k-')
    
    minFit = np.polyfit(hot['bulk_strain'], hot['den_min'], 1)
    regFit = np.polyfit(hot['bulk_strain'], hot['den_strain'], 1)
    maxFit = np.polyfit(hot['bulk_strain'], hot['den_max'], 1)
    minY = minFit[0] * x + minFit[1]
    #regY = regFit[0] * x + regFit[1]
    regY = 0.5751 * x;
    maxY = maxFit[0] * x + maxFit[1]
    ax.plot(x, regY, 'k-')
    ax.plot(x, maxY, 'k--')
    
    #plots Jesi's strain data on the linear regression of my data
    ax.plot([0.20, 0.31], [regFit[0] * 0.20 + regFit[1], regFit[0] * 0.31 + regFit[1]], 'w^')
    
    ax.legend(['reference', 'strain y = 0.5834x, Adj R-squared = 0.9436 ', '1 ' + r'${\sigma}$','EBSD strain'], 2, fontsize = 16)
    ax.plot(x, minY, 'k--')
    
def main():
    data = pandas.read_csv('bulk_den_strain.csv', sep = ",", header = 0)
    #room = pandas.read_csv('bulk_den_strain_rt.csv', sep = ",", header = 0)

    data['den_min'] = (((data['AR'] - data['std']) / 1.324021) ** .5) -1
    data['den_max'] = (((data['AR'] + data['std']) / 1.324021) ** .5) -1
    
    #den_vs_bulk_strain(data)
    ave_ar_vs_strain(data)
    