# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 13:54:45 2015

@author: Rachel
"""

import pandas 
import numpy as np
import matplotlib.pyplot as plt

def plot_histogram_for_region(data, subRegions, region):
    '''
    Plots a histogram for a strain region specified by a list of subregions. Returns an frame of ratios, the mean, and standard deviation
    of  the subregion.
    
    usage: ratios, mean, std-dev = plot_histogram_for_region(ellipseDataFrame, listOfSubRegions, intRegionNumber)
    '''
    subFrame = pandas.DataFrame()
    for i in subRegions:
        temp = data[data['location'] ==  i]
        subFrame = subFrame.append(temp)
    ratios = subFrame['aspect_ratio']
    ratiosFrame = pandas.DataFrame(ratios)  
    ax = ratiosFrame.plot( kind = 'hist', title = ('Dendrite Aspect Ratios for Region ' + str(region)), bins = 20 
                      , xticks = [x for x in xrange(1,11)], yticks = [y for y in xrange(1,25)], legend = False)
    ax.set_xlabel('Aspect Ratio')
    return (ratios, ratios.mean(), ratios.std())
    
def plot_daily_average(data):
    '''
    Plots a graph of the average dendrite aspect ratio per day with error bars of the standard deviation.

    usage: plot_daily_average(dendriteData)
    '''
    index = 1
    dates = data['date']
    allData = []
    dates = sorted(list(set(data['date'])))
    print(type(dates[0]))
    for date in dates: 
        dateFrame = data[data['date'] == date]
        base = dateFrame[dateFrame['location'] == 13]
        mean = base['aspect_ratio'].mean()
        std = base['aspect_ratio'].std()
        allData.append([index, date, mean, std]) 
        index = index + 1
    allFrame = pandas.DataFrame(allData, columns = ['index', 'date', 'mean', 'std_dev'])
    ax = allFrame.plot(kind = 'scatter',x = 'index', y = 'mean', yerr = 'std_dev', title = 'Daily Baseline Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average Aspect Ratio')
    dates = [' '] + dates
    ax.set_xticklabels(dates)
    
def plot_daily_distribution(data):
    '''
    Plots a box and whisker plot of the daily baseline aspect ratios.
    
    usage: plot_daily_distributaion(dendriteData)
    '''    
    frames = []
    dates = sorted(list(set(data['date'])))
    for date in dates: 
        #slice frame by date
        dateFrame = data[data['date'] == date]
        #slice date frame by baseline location
        base = dateFrame[dateFrame['location'] == 13]
        length = base.shape[0]
        #aspect ratio of base
        temp = base['aspect_ratio']
        tempF = pandas.DataFrame(temp)
        tempF.set_index(np.arange(length), inplace = True)
        tempF.columns = [date]
        frames.append(tempF)
    allData = pandas.concat(frames, axis = 1)
    ax = allData.plot(kind = 'box', title = 'Daily Distribution')
    ax.set_xlabel('Date')
    ax.set_ylabel('Aspect Ratio')

def plot_histograms(data):
    '''
    Plots the histrogram for each region and returns the stats (mean and std) for each region
    
    usage: stats = plot_histograms(dendriteData)
    '''
    frame5, mean5, std5 = plot_histogram_for_region(data, [2, 3, 4, 5, 6], 3)
    frame4, mean4, std4 = plot_histogram_for_region(data, [7, 8, 9, 10, 11, 12, 13], 2)      
    frame3, mean3, std3 = plot_histogram_for_region(data, [14, 15, 16, 17, 18, 19, 20], 1)
    frame2, mean2, std2 = plot_histogram_for_region(data, [16, 17, 18, 19, 20], 2)
    frame1, mean1, std1 = plot_histogram_for_region(data, [21, 22, 23, 24, 25], 1)
    stats = pandas.DataFrame([[1, mean1, std1], [2, mean2, std2], [3, mean3, std3], [4, mean4, std4], [5, mean5, std5]], columns = ['region', 'mean', 'std'])

    plt.close('all')    
    
    return stats
    
def plot_region_average(stats):
    '''
    Plots the average and standard deviation (as error bars) for each strain region of the sample. Pass in a data
    frame with the columns region, mean, and std.
    
    usage: plot_region_average(stats)
    '''
    ax = stats.plot(kind = 'scatter', title = 'Region Aspect Ratio Average', x = 'region', y = 'mean', yerr = 'std')    
    ax.set_xlabel('Region')
    ax.set_ylabel('Average Aspect Ratio') 
    labels = ['undeformed', '1',' ',  '2',' ', '3', 'deformed']
    ax.set_xticklabels(labels)

def plot_strain_average(stats, strains):
    '''
    Plots the average aspect ratio vs. strain. 
    
    usage: plot_strain_average(stats, strains)
    ''' 
    
    stats['strains'] = pandas.Series(strains, index = stats.index)
    ax = stats.plot(kind = 'scatter', title = 'Average Aspect Ratio vs. Strain', x = 'strains', y = 'mean', yerr = 'std')    
    ax.set_xlabel('Strain')
    ax.set_xlim([0, 1])
    ax.set_ylabel('Average Aspect Ratio')
    ax.set_ylim([1, 5.5])
    fit = np.polyfit(stats['strains'], stats['mean'], 2)
    x = np.linspace(0, 1, 20) 
    y = fit[2] + (fit[1] * x) + (fit[0] * (x**2)) 
    ax.plot(x, y, 'r-')
    ax.legend(['raw',' y = {0}x^2 + {1}x + {2}'.format("{:.2f}".format(fit[0]), "{:.2f}".format(fit[1]), "{:.2f}".format(fit[2]))], 2)
    
def plot_dendrite_vs_bulk_strain(stats):
    '''
    Calculates the strain of a region of dendrites given a dataframe of aspect ratio values. Strains are appended as new column in dataframe.
    TODO: add error bars?
    usage: plot_dendrite_vs_bulk_strain(stats)
    '''
    stats['dendrite_strain'] = (stats['mean'] ** .5) - 1
    stats['den_min'] = ((stats['mean'] - stats['std']) ** .5) -1
    stats['den_max'] = ((stats['mean'] + stats['std']) ** .5) -1
    print(stats)
    ax = stats.plot(kind = 'scatter', title = 'Dendrite Strain vs. Bulk Strain', x = 'bulk_strain', y = 'dendrite_strain')
    ax.set_xlabel('Bulk Strain')
    ax.set_xlim([0, 1])
    ax.set_ylabel('Dendrite Strain')
    ax.set_ylim([0, 1.3])
    ax.plot([0, 1], [0, 1], 'r-') 
    
    x = np.linspace(0, 1, 20) 
    minFit = np.polyfit(stats['bulk_strain'], stats['den_min'], 1)
    regFit = np.polyfit(stats['bulk_strain'], stats['dendrite_strain'], 1)
    maxFit = np.polyfit(stats['bulk_strain'], stats['den_max'], 1)
    minY = minFit[0] * x + minFit[1]
    regY = regFit[0] * x + regFit[1]
    maxY = maxFit[0] * x + maxFit[1]
    ax.plot(x, minY, 'g-')
    ax.plot(x, regY, 'b-')
    ax.plot(x, maxY, 'm-')

    ax.plot(stats['bulk_strain'], stats['den_min'], 'go')
    ax.plot(stats['bulk_strain'], stats['den_max'], 'mo')
    ax.legend(['reference', 'min', 'strain', 'max'], 2)
    
def main():
    d = pandas.read_csv('BMGMC_dendrite_data_with_locations.csv', sep = ",", header = 0)
    #adds new column of aspect ratios to data frame
    d['aspect_ratio'] = d['long_axis'] / d['short_axis']  
    #print(d.mean())
    #print(d.std())
    
    #hot_strains = [.4608, .5597, .6553, .7795, .9383]
    #RT_strains = [.1726, .4692, .8182]
    stats = plot_histograms(d)
    print(stats)
    #plot_region_average(stats)
    #add bulk strain column to stats frame
    #stats['bulk_strain'] = [.1726, .4692, .8182]
    #plot_strain_average(stats, RT_strains)
    #plot_dendrite_vs_bulk_strain(stats)
   
    
