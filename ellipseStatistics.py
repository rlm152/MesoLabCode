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
    #if(longAxisArray.size != shortAxisArray.size):
        #print("ERROR: invalid inputs. Arrays must be equal length")
        #return
    ratios = []
    counter = 0
    for i in longAxisArray:
        ratios.append(float(longAxisArray.iloc[counter]) / float(shortAxisArray.iloc[counter]))
        counter = counter + 1
    return pandas.DataFrame(ratios)

def plotHistogramForRegion():
    return 0

def main():
    dendriteData = read_csv_file("BMGMC_dendrite_data_with_locations.csv")
    bounds = slice_frame_by_attribute(dendriteData.iloc[1:, 1], "4")
    aR4 = calculate_aspect_ratio(dendriteData.iloc[bounds[0]:bounds[1], 5], dendriteData.iloc[bounds[0]:bounds[1], 6])
    pandas.DataFrame.hist(aR4, column=None, by=None, grid=True, xlabelsize=None, xrot=None, ylabelsize=None, yrot=None, ax=None, sharex=False, sharey=False, figsize=None, layout=None, bins=5)
    aR4.plot(kind = "hist", stacked = True, bins = 5)

