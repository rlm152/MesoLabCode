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
    ax = hot.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', yerr = 'std', color = 'k')    
    ax.set_xlabel('Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Average Aspect Ratio', fontsize = 20)
    ax.set_ylim([1, 5])
    fit = np.polyfit(hot['bulk_strain'], hot['AR'], 1)    
    x = np.linspace(0, 1, 20) 
    y = fit[1] + (fit[0] * x) 
    print(y)
    ax.plot(x, y, 'k--')
    ax.legend(['raw',' y = {0}x + {1}'.format("{:.2f}".format(fit[0]), "{:.2f}".format(fit[1]))], 2, fontsize = 14)


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
    #'''Trying to see if we can use linear models to help get the correct r squared value
   # model = lm.LinearRegression(fit_intercept = False)
   # bulk_strain_array = np.array([hot['bulk_strain'][region] for region in hot['bulk_strain'].index])
   # dendrite_strain_array = np.array([hot['den_strain'][region] for region in hot['den_strain'].index])
   # model.fit(bulk_strain_array, dendrite_strain_array)
    #ax.plot(bulk_strain_array, model.predict(bulk_strain_array), color = 'r')'''
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
    
    ax.legend(['reference', 'strain y = 0.5751x, Adj R-squared = 0.9886', '1 ' + r'${\sigma}$','EBSD strain'], 2, fontsize = 16)
    ax.plot(x, minY, 'k--')
    
def lin_fit(x, y):
    '''Fits a linear fit of the form mx+b to the data'''
    fitfunc = lambda params, x: params[0] * x + params[1]    #create fitting function of form mx+b
    errfunc = lambda p, x, y: fitfunc(p, x) - y              #create error function for least squares fit

    init_a = 0.5                            #find initial value for a (gradient)
    init_b = 0                              #find initial value for b (y axis intersection)
    init_p = np.array((init_a, init_b))     #bundle initial values in initial parameters

    #calculate best fitting parameters (i.e. m and b) using the error function
    p1, success = sp.optimize.leastsq(errfunc, init_p.copy(), args = (x, y))
    f = fitfunc(p1, x)          #create a fit with those parameters
    return p1, f  
    
def main():
    data = pandas.read_csv('bulk_den_strain_hot.csv', sep = ",", header = 0)
    #room = pandas.read_csv('bulk_den_strain_rt.csv', sep = ",", header = 0)

    data['den_min'] = (((data['AR'] - data['std']) / 1.324021) ** .5) -1
    data['den_max'] = (((data['AR'] + data['std']) / 1.324021) ** .5) -1
    
    den_vs_bulk_strain(data)
    #ave_ar_vs_strain(hot)
    