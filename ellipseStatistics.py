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

    #
    for d in frame:
        if startNotSet and d == att:

            startIndex = counter
            startNotSet = False
            
        #print(startNotSet)
        if startNotSet == False and d != att:
            endIndex = counter - 1
            break
        counter = counter + 1  
    if endIndex == 0:
        endIndex = counter - 1
    return [startIndex, endIndex]
    
def calculateAspectRatio(longAxisArray, shortAxisArray):
    """
    Returns a list of aspect ratio values.
    
    usage: ratios = calculateAspectRatio(longAxisArray, shortAxisArray)
    """
    if(len(longAxisArray) != len(shortAxisArray)):
        print("ERROR: invalid inputs. Arrays must be equal length")
        return
    ratios = []
    for i in longAxisArray:
        ratios.append(longAxisArray[i] / shortAxisArray[i])
    return ratios
    

def main():
    dendriteData = read_csv_file("BMGMC_dendrite_data_with_locations.csv")

    bounds = slice_frame_by_attribute(dendriteData.iloc[1:, 1], "4")
    print(bounds)
    
    
    #print(dendriteData.iloc[bounds[0]:bounds[1], 2])
    #print(dendriteData.iloc[0:, 0:2])
