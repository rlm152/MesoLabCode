# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:12:31 2015

@author: Rachel
"""

from scipy import ndimage
from skimage.measure import moments
import numpy as np
import csv
import datetime

def fit_ellipse(data):
    '''
    Returns the length of the long and short axis and the angle measure
    of the long axis to the horizontal of the best fit ellipsebased on
    image moments.
    
    usage: longAxis, shortAxis, angle = fit_ellipse(N_by_M_image_as_array)
    '''
    # source:
    #     Kieran F. Mulchrone, Kingshuk Roy Choudhury,
    # Fitting an ellipse to an arbitrary shape:
    # implications for strain analysis, Journal of
    # Structural Geology, Volume 26, Issue 1,
    # January 2004, Pages 143-153, ISSN 0191-8141,
    # <http://dx.doi.org/10.1016/S0191-8141(03)00093-2.>
    #     Lourena Rocha, Luiz Velho, Paulo Cezar P. Carvalho
    # Image Moments-Based Structuring and Tracking of
    # Objects, IMPA-Instituto Nacional de Matematica Pura
    # e Aplicada. Estrada Dona Castorina, 110, 22460
    # Rio de Janeiro, RJ, Brasil,
    # <http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1167130>

    m = moments(data, 2) # super fast compated to anything in pure python
    xc = m[1,0] / m[0,0]
    yc = m[0,1] / m[0,0]
    a = (m[2,0] / m[0,0]) - (xc**2)
    b = 2 * ((m[1,1] / m[0,0]) - (xc * yc))
    c = (m[0,2] / m[0,0]) - (yc**2)
    theta = .5 * (np.arctan2(b, (a - c)))
    w = np.sqrt(6 * (a + c - np.sqrt(b**2 + (a-c)**2)))
    l = np.sqrt(6 * (a + c + np.sqrt(b**2 + (a-c)**2)))
    return xc, yc, l, w, theta

def read_image(imageName):
    '''
    Reads a .png file an integer array. The image name input must contain the proper file type extension.
    
    usage: floatArray = read_image(imageName)
    '''
    imageArray = ndimage.imread(imageName, flatten = True)
    return imageArray 
    
#returns a labled 
def label_components(imageArray):
    '''
    Take an array and returns an integer array with the connected components labled with unique integers.
    
    usage: labledArray = label_components(array)
    '''
    return ndimage.label(imageArray)


def isolate_component(imageArray, index):
    '''
    Takes an array with labeled connected components and isolates a particular integer labeled component.
    Returns a float64 array with a single connected component. 
    
    usage: isolatedArray = isolate_component(labeledArray, isolationIntegerIndex)
    '''
    imageArray = np.array([[(0 if not col == index else col) for col in row] for row in imageArray])
    #typecasting array into float64 so it can be used in fit_ellipse
    imageArray = np.array([[np.float64(col) for col in row] for row in imageArray])
    return imageArray

#generates column labels for the csv file, returns label as a list
def generate_column_labels():
    '''
    Generates data column labels for a csv file. Returns a list of labels.
    
    usage: listOfLabels = generate_column_labels()
    '''
    labels = [];
    labels.append("file_name")
    labels.append("date")
    labels.append("x_coordinate")
    labels.append("y_coordinate")
    labels.append("long_axis")
    labels.append("short_axis")
    labels.append("angle")
    return labels
    
def erode_and_dialate(imageArray):
    '''
    Erodes and dialates an image using a basic binary structure.
    
    usage: processedArray = erode_and_dialate(imageArray)
    '''
    structEl = ndimage.generate_binary_structure(2, 1)
    structEl = structEl.astype(imageArray.dtype)
    erodeAndDialate = ndimage.binary_dilation(ndimage.binary_erosion(imageArray, structEl), structEl)
    erodeAndDialate = erodeAndDialate.astype(imageArray.dtype)
    return erodeAndDialate
        
def main(): 
    imageName = "noisyImage"
    print(imageName)
    #imageName = input("Please enter a filename (with quotes): ")
    #print("Thank you.")
    #date = datetime.date.today()
    date = datetime.date(2015, 7, 7)
    print(date)
    generateLabels = input("Labels? (True or False): ")
    #reads the image into an array of pixel values
    imageRead = read_image(imageName + ".png")
    #removes small artifacts from image
    cleanImage = erode_and_dialate(imageRead)
    #labels the connected components
    image, numLabel = label_components(cleanImage)    
    #opens a csv file to which the data points will be appended
    with open("smallFile.csv","a") as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        #generates column labels for csv file if desired
        if(generateLabels):
            writer.writerow(generate_column_labels())
        #analyzes each ellipse in the image and stores the cooresponding data 
        for x in range(numLabel):
            whiteOutArray = isolate_component(image, x + 1)
            xc, yc, longAxis, shortAxis, angle = fit_ellipse(whiteOutArray)
            info = [];
            info.append(imageName)
            info.append(date)
            info.append(xc)
            info.append(yc)
            info.append(longAxis)
            info.append(shortAxis)
            info.append(angle)
           # print("x coordinate: {0}\ny coordinate: {1}\nlong axis: {2}\nshort axis: {3}".format(xc, yc, longAxis, shortAxis))
            writer.writerow(info)
    print("All done!")
            

    
    
        

