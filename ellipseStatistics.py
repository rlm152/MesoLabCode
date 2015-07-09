# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 13:54:45 2015

@author: Rachel
"""

import pandas 
import datetime

def read_csv_file(filename):
    """
    Reads a csv file into a data frame
    """
    dendriteData = pandas.read_csv(filename, sep = ",", header = None)
    return dendriteData

def slice_frame_by_attribute(frame, att):
    """
    Slices the data frame by date and returns a starting and ending indicies for subframe 
    """
   #print(frame)
    startNotSet = True
    counter = 0
    startIndex = 0
    endIndex = 0
    #typecast date from datetime object to string so it can be compared to d
    att = str(att)
    print(att)
    
    #
    for d in frame:
        if startNotSet and d == att:
            startIndex = counter
            print(startIndex + " yay")
            startNotSet = False
        if startNotSet == False and d != att:
            endIndex = counter
            break
        counter = counter + 1  
    if endIndex == 0:
        endIndex = counter
    return [startIndex, endIndex]
    
def main():
    dendriteData = read_csv_file("BMGMC_dendrite_data_with_locations.csv")
    bounds = slice_frame_by_attribute(dendriteData.iloc[1:, 2], datetime.date(2015, 7, 7))
    print(bounds)
    #print(dendriteData.iloc[bounds[0]:bounds[1], 2])
   # print(dendriteData.iloc[0:, 0:2])
