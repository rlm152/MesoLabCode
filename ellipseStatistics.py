# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 13:54:45 2015

@author: Rachel
"""

import pandas 
import numpy as np

def read_csv_file(filename):
    """
    Reads a csv file into a data frame
    """
    dendriteData = pandas.read_csv(filename, sep = ",", header = None)
    return dendriteData

def slice_frame_by_attribute(frame, att):
    """
    Slices the data frame by attribute and returns a starting and ending indicies for subframe .
    Will only find the first grouping of a particular attribute. 
    
    TODO: deal with the fact that there are multiple baslines locations!!!
    
    usage: bounds = slice_fram_by_attribute(frame, attributeAsAString)
    """
    startNotSet = True
    counter = 1
    startIndex = 0
    endIndex = 0

    #cycles through the items in the frame and finds the start and end of a group of an attribute
    for d in frame:
        if startNotSet and d == att:
            startIndex = counter
            startNotSet = False
        if startNotSet == False and d != att:
            endIndex = counter
            break
        counter = counter + 1  
    if endIndex == 0:
        endIndex = counter
    return [startIndex, endIndex]
    
def calculate_aspect_ratio(longAxisArray, shortAxisArray):
    """
    Returns a data frame of aspect ratio values.
    
    usage: ratios = calculate_aspect_ratio(longAxisArray, shortAxisArray)
    """
    ratios = []
    counter = 0
    for i in longAxisArray:
        ratios.append(float(longAxisArray.iloc[counter]) / float(shortAxisArray.iloc[counter]))
        counter = counter + 1
    return pandas.DataFrame(ratios)

def plot_histogram_for_region(data, subRegions, region):
    """
    Plots a histogram for a strain region specified by a list a subregions. Returns an array with the mean and standard deviation.
    
    usage: plot_histogram_for_region(ellipseDataFrame, listOfSubRegions, intRegionNumber)
    """
    aspectRatios = []
    for i in subRegions:
        bounds = slice_frame_by_attribute(data.iloc[1:, 1], str(i))
        #column 5 is long axes, column 6 is short axes
        subRatio = calculate_aspect_ratio(data.iloc[bounds[0]:bounds[1], 5], data.iloc[bounds[0]:bounds[1], 6])
        aspectRatios.append(subRatio)

    aRFrame = pandas.concat(aspectRatios)
    ax = aRFrame.plot(kind = "hist", title = ("Dendrite Aspect Ratios for Region " + str(region)), bins = 20 
                      ,xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], yticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], legend = False)
    ax.set_xlabel("Aspect Ratio")
    return (aRFrame, aRFrame.mean(), aRFrame.std())
    

def daily_mean_and_std(data, day):
    """
    Calculates the standard deviation for a given day. 
    
    usage: daily_std = (dataFrameOfData, dayAsString)
    """
    #bounds for a particular day
    dBounds = slice_frame_by_attribute(data.iloc[1:, 2], day)
    #frame of all data for day
    dFrame = data.iloc[dBounds[0]:dBounds[1], :]
    #bounds within day for baseline region (13)
    rBounds = slice_frame_by_attribute(dFrame.iloc[:, 1], "13")
    #frame of all data for day and baseline region
    dRFrame = dFrame.iloc[rBounds[0] - 1 : rBounds[1] - 1 , :]
    ratios = calculate_aspect_ratio(dRFrame.iloc[:, 5], dRFrame.iloc[:, 6])
    return ratios.mean(), ratios.std()

def plot_daily_average(data):
    """
    Plots a graph of the average dendrite aspect ratio per day with error bars of the standard deviation.
    
    usage: plot_daily_average(dendriteData)
    """
    days = pandas.DataFrame(["6/24/2015", "7/1/2015", "7/2/2015", "7/6/2015", "7/7/2015"], columns = np.array(['a']))
    means = []
    stds = []
    print(days.iterrows())
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

def main():
    
    dendriteData = read_csv_file("BMGMC_dendrite_data_with_locations.csv")
    plot_daily_average(dendriteData)
    '''
    frame1, mean1, std1 = plot_histogram_for_region(dendriteData, [3, 4, 5], 1)
    frame2, mean2, std2 = plot_histogram_for_region(dendriteData, [6, 7, 8, 9, 10], 2)      
    frame3, mean3, std3 = plot_histogram_for_region(dendriteData, [11, 12, 13, 14, 15], 3)
    frame4, mean4, std4 = plot_histogram_for_region(dendriteData, [16, 17, 18, 19, 20], 4)
    frame5, mean5, std5 = plot_histogram_for_region(dendriteData, [21, 22, 23, 24, 25], 5)
    
    stats = pandas.DataFrame([[mean1, std1], [mean2, std2], [mean3, std2], [mean4, std4], [mean5, std5]])
    print(stats)
    '''
    print(daily_mean_and_std(dendriteData, "7/1/2015"))