# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 13:54:45 2015

@author: Rachel
"""

import pandas 
import numpy as np

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
                      , xticks = [x for x in xrange(1,11)], yticks = [y for y in xrange(1,18)], legend = False)
    ax.set_xlabel('Aspect Ratio')
    return (ratios, ratios.mean(), ratios.std())
    
def plot_daily_average(data):
    '''
    Plots a graph of the average dendrite aspect ratio per day with error bars of the standard deviation.
    TODO:FIX NEW SLICING
    usage: plot_daily_average(dendriteData)
    '''
    allData = []
    dates = sorted(list(set(data['date'])))
    print(dates)
    for date in dates: 
        dateFrame = data[data['date'] == date]
        base = dateFrame[dateFrame['location'] == 13]
        mean = base['aspect_ratio'].mean()
        std = base['aspect_ratio'].std()
        allData.append([date, mean, std])
        
    allFrame = pandas.DataFrame(allData, columns = ['date', 'mean', 'std_dev'])
    ax = allFrame.plot(kind = 'scatter', x = 'date', y = 'mean', title = 'Daily Baseline Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Average')

    '''
    #days = pandas.DataFrame(['6/24/2015', '7/1/2015', '7/2/2015', '7/6/2015', '7/7/2015'], columns = np.array(['date']))
    means = []
    stds = []
    for i, day in days.iterrows():
        print(day)
        mean, std = daily_mean_and_std(data, str(day))
        means.append(mean)
        stds.append(std)
    #print(days)
    #print(means)
    dm = pandas.DataFrame(means)
    print(dm)
    dm.columns = np.array(['b'])
    ds = pandas.DataFrame(stds)
    ds.columns = np.array(['c'])
    print(ds)
    #print(dm)
    print(pandas.concat([days, dm, ds], axis = 1, join_axes = [days.index]))
   # print(stds)
   # dailyData = pandas.concat(frames)
   # print(dailyData)
    #ax = means.plot(kind = "scatter", title = "Daily Average Dendrite Aspect Ratio" )
'''

def plot_histograms(data):
    '''
    Plots the histrogram for each region and returns the stats (mean and std) for each region
    
    usage: stats = plot_histograms(dendriteData)
    '''
    frame1, mean1, std1 = plot_histogram_for_region(data, [3, 4, 5], 1)
    frame2, mean2, std2 = plot_histogram_for_region(data, [6, 7, 8, 9, 10], 2)      
    frame3, mean3, std3 = plot_histogram_for_region(data, [11, 12, 13, 14, 15], 3)
    frame4, mean4, std4 = plot_histogram_for_region(data, [16, 17, 18, 19, 20], 4)
    frame5, mean5, std5 = plot_histogram_for_region(data, [21, 22, 23, 24, 25], 5)
    
    stats = pandas.DataFrame([[1, mean1, std1], [2, mean2, std2], [3, mean3, std2], [4, mean4, std4], [5, mean5, std5]], columns = ['region', 'mean', 'std'])
    return stats
    
def main():
    d = pandas.read_csv('BMGMC_dendrite_data_with_locations.csv', sep = ",", header = 0)
    #adds new column of aspect ratios to data frame
    d['aspect_ratio'] = d['long_axis'] / d['short_axis']   
    plot_daily_average(d)
    
