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
    
    
def main():
    dendriteData = read_csv_file("BMGMC_dendrite_data.csv")
    print(dendriteData.iloc[1:, 1])