# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 13:54:45 2015

@author: Rachel
"""

import pandas 

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
    ax = aRFrame.plot(kind = "hist", title = ("Dendrite Aspect Ratios for Region " + str(region)), bins = 20, xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], legend = False)
    ax.set_xlabel("Aspect Ratio")
    return (aRFrame, aRFrame.mean(), aRFrame.std())
    

    

def main():
    dendriteData = read_csv_file("BMGMC_dendrite_data_with_locations.csv")
    frame1, mean1, std1 = plot_histogram_for_region(dendriteData, [3, 4, 5], 1)
    frame2, mean2, std2 = plot_histogram_for_region(dendriteData, [6, 7, 8, 9, 10], 2)      
    frame3, mean3, std3 = plot_histogram_for_region(dendriteData, [11, 12, 13, 14, 15], 3)
    frame4, mean4, std4 = plot_histogram_for_region(dendriteData, [16, 17, 18, 19, 20], 4)
    frame5, mean5, std5 = plot_histogram_for_region(dendriteData, [21, 22, 23, 24, 25], 5)
    
    stats = pandas.DataFrame([[mean1, std1], [mean2, std2], [mean3, std2], [mean4, std4], [mean5, std5]])
    print(stats)
    
