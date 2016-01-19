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
from scipy.interpolate import interp1d

def ave_ar_vs_strain(hot, room):
    
    ax = hot.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', yerr = 'std', facecolors = 'b', edgecolors = 'k', grid = 'off', marker = 'o')           
    x = np.linspace(-1, 1, 20) 
    offset = 1.324021
    model = pandas.ols(y = hot['AR'], x = hot['bulk_strain'], intercept = False)
    hot['fit'] = model.y_fitted    
    hot['AR_with_offset'] = hot['AR'] - offset
    model_offset = pandas.ols(y = hot['AR_with_offset'], x = hot['bulk_strain'], intercept = False)
    y = 1.8728 * x + offset
    room.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', yerr = 'std', edgecolors = 'k', facecolors = 'c', grid = 'off', ax = ax, marker = 'o')
    #room.plot(kind = 'scatter', x = 'bulk_strain', y = 'AR', edgecolors = 'k', facecolors = 'c', grid = 'off', ax = ax, marker = 'o')
    #ax.plot(room['bulk_strain'], room['AR'], 'wo', yerr = room['std'])
    ax.plot(x, y, 'r--')
    degree_sign= u'\N{DEGREE SIGN}'
    
    ax.set_xlabel('Strain', fontsize = 20)
    ax.set_xlim([-0.01, 1])
    ax.set_ylabel('Average Aspect Ratio', fontsize = 20)
    ax.set_ylim([1, 5])
    ax.legend(['603 K (330'+ degree_sign + 'C)','298 K (25' + degree_sign + 'C)'], 2, fontsize = 14)


def den_vs_bulk_strain(hot):
    '''
    plots the dendrite vs. bulk strain given a data frame
    
    '''
 
    ax = hot.plot(kind = 'scatter',  x = 'bulk_strain', y = 'den_strain', color = 'b', grid = 'off', edgecolors = 'k')
    ax.set_xlabel('Bulk Strain', fontsize = 20)
    ax.set_xlim([0, 1])
    ax.set_ylabel('Dendrite Strain', fontsize = 20)
    ax.set_ylim([0, 1])
    ax.plot([0, 1], [0, 1], 'y')

    x = np.linspace(0, 1, 20)
    
    model_no_intercept = pandas.ols(y = hot['den_strain'], x = hot['bulk_strain'], intercept = False)
    #print(model_no_intercept)
    hot['fit'] = model_no_intercept.y_fitted
    #ax.plot(hot['bulk_strain'], hot['fit'], 'k-')
    
    minFit = np.polyfit(hot['bulk_strain'], hot['den_min'], 1)
    regFit = np.polyfit(hot['bulk_strain'], hot['den_strain'], 1)
    maxFit = np.polyfit(hot['bulk_strain'], hot['den_max'], 1)
    minY = minFit[0] * x + minFit[1]
    #unadjusted hot fit
    #regY = 0.5751 * x;
    #adjusted hot fit
    regY = 0.6140 * x    
    maxY = maxFit[0] * x + maxFit[1]
    ax.plot(x, regY, 'b')
    ax.plot(x, maxY, 'g')
    
    #plots Jesi's strain data on the hot linear regression of my data
    ax.plot([0.20, 0.31], [0.1228, 0.19034], 'm^')
    #unadjusted room strain
    #ax.plot([0.053397, 0.056683,0.064545], [0.078187, 0.136025, 0.168882], 'wo')
    #adjusted room strain
    ax.plot([0.09813, 0.10130,0.10886], [0.078187, 0.136025, 0.168882], 'co')
    degree_sign= u'\N{DEGREE SIGN}'
    ax.legend(['reference', '603 K (330' + degree_sign + 'C)', '1 ' + r'${\sigma}$','EBSD strain', '298 K (25' + degree_sign + 'C)'], 2, fontsize = 16)
    ax.plot(x, minY, 'g')
    
    
def plot_BMG_BMGMC_stress_strain(data):
    
    plot_two_columns(data,'BMG_27_strain','BMG_27_stress')
    plot_two_columns(data,'BMG_330_strain','BMG_330_stress')
    plot_two_columns(data,'BMGMC_27_strain','BMGMC_27_stress')
    plot_two_columns(data,'BMGMC_330_strain','BMGMC_330_stress')
    

def plot_two_columns(data,col1,col2):
    data = data[pandas.notnull(data[col2])]
    
    x = [(float(z[0]) if float(z) > 0 else 0.0) for z in data[[col1]].values]
    y = [(float(z[0]) if float(z) > 0 else 0.0) for z in data[[col2]].values]
    x, y = (list(t) for t in zip(*sorted(zip(x,y))))

    print(x, y)
    
    fxn = interp1d(x, y, kind = 'nearest')
    
    plt.plot(x, fxn(x), '-')
    
    #print(data[[col1]].values,data[[col2]].values)
    
    
def main():
    data = pandas.read_csv('bulk_den_strain_adjusted_hot.csv', sep = ",", header = 0)
    #room = pandas.read_csv('bulk_den_strain_rt.csv', sep = ",", header = 0)

    data['den_min'] = (((data['AR'] - data['std']) / 1.324021) ** .5) -1
    data['den_max'] = (((data['AR'] + data['std']) / 1.324021) ** .5) -1
    #print(data)
   # den_vs_bulk_strain(data)
    
    hot = pandas.read_csv('bulk_den_strain_adjusted_hot.csv', sep = ',', header = 0)
    room = pandas.read_csv('bulk_den_strain_adjusted_room_with_zero.csv', sep = ',', header = 0)
    #ave_ar_vs_strain(hot, room)
    
    jesiData = pandas.read_csv('corrected_BMG_BMGMC_stress_strain.csv', sep = ",", header = 0)
    #print(jesiData.columns)
    #print([(float(z[0]) if float(z) > 0 else 0.0) for z in jesiData[['BMG_330_stress']].values])
    
    plot_BMG_BMGMC_stress_strain(jesiData)
    