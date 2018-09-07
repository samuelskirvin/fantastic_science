#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrieving and investigating the catalog data

Challenge description:

The astroquery package has an interface to the Infrared 
Science Archive (IRSA) which is a large archive of many 
infrared datasets. One of these datasets is a Galactic plane 
survey from the MSX satellite.

Use astroquery to find out what catalogs are available from IRSA. 
For each catalog, you’ll likely find out a short name 
(e.g. akari_fis and a longer name, e.g. Akari/FIS Bright Source 
Catalogue). Find out what catalogs are available for MSX. 
[Hint: you can search for MSX or Midcourse in the long name - 
and bonus points if you don’t do that by hand!].
Keep track of the short name for the catalog that doesn’t contain
rejected sources (this will make sense once you see the available 
catalogs)
Next up, do a ‘box’ search at the position of M16, with a size of 1 
degree, from the main MSX catalog. You may run into an issue where 
there are too many rows being returned (see here for information on 
getting around this issue). How many rows did the query return?
Make a scatter plot of the positions of the sources on the sky using 
their Right Ascension and Declination.
The table includes columns called q_a and q_c that give the quality 
of the photometry in bands A and C (where 2 and above is good). 
Filter the table to include only rows where these two values are 
greater or equal to 2. How many rows remain? You can try and update 
your plot of the positions.
The a, c, d, and e bands give the fluxes at 3.4, 4.6, 12, and 22µm 
respectively. Split the table into two sets of sources: those that 
have c/a>1.5, and the remaining sources. Next up, plot the positions 
of each set of sources and compare their distributions.
Write a Python script that contains a function that given the 
parameters for the astroquery search (position and width), will 
return the two groups of sources for the MSX catalog, and share this 
function with your co-worker (ideally via a shared git repository!).

@author: andrechicrala
"""

#importing the packages
from astroquery.irsa import Irsa
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

def what_msx_catalogs():
    '''
    This function lists the ISRA catalogs.
    '''

    #listing the catalogs
    catalog = Irsa.list_catalogs()
    
    #taking the keys that have
    keys = [k for k in catalog.keys() if 'msx' in k]
    
    #taking the msx catalogs
    msx_catalogs = {keys[0]: catalog[keys[0]],
                    keys[1]: catalog[keys[1]]}
    

    return(msx_catalogs)


def msx_in_box(region = None, msx_catalog = None):
    '''
    This function will get the desired data
    using a msx_in_box search in 1 deg.
    '''
    
    #here we will check if no values
    #were given and default them if not.
    if region is None:
        region = 'M16'
    
    if msx_catalog is None:
        msx_catalog = list(what_msx_catalogs().keys())[0] 
        
    
    #modifying the limit for the Isra query
    Irsa.ROW_LIMIT = 1000
    
    #creating a table for the box search
    table = Irsa.query_region(region, catalog = msx_catalog, 
                              spatial = 'Box', width = 1 * u.deg)
    
    #printing the number of rows
    print('The number of rows in this data set is: ', np.shape(table)[0])
    
    return(table)


def scattering(table = None):
    '''
    This function makes a scatter plot of 
    the positions of the sources on the 
    sky using their Right Ascension and 
    Declination.
    '''
    
    #here we will check if no values
    #were given and default them if not.
    if table is None:
        table = msx_in_box
        
    #making the plot function
    def plot_function(x,y, title):
        img = plt.figure(figsize = (8,8))
        plt.scatter(x, y)
        plt.title(title)
        plt.xlabel('Declination')
        plt.ylabel('Right Ascension')
        plt.show(img)
        return()

    #making the first plot
    plot_function(x = table['ra'], y = table['dec'], 
                  title = 'Sources positions')
    
    #creating empty arrays to stash
    #the filtered data
    filt_ra = []
    filt_dec = []
    
    #filtering the data
    for line in zip(table['ra'], table['dec'], table['q_a'], table['q_c']):
        #stating the filter
        if line[2] and line[3] >= 2:
            #appending the results to the lists
            filt_ra.append(line[0])
            filt_dec.append(line[1])
        
    #plotting again
    plot_function(filt_ra, filt_dec, title = 'Filtered Sources Positions')
    
    return(filt_ra, filt_dec)
    
    #printing the number of results
    print('The number of elements in the filtered tables is: ', len(filt_ra))

if __name__ == '__main__':
    '''
    test zone!
    '''
    
    #testing if what_msx_catalogs works!
    #msx_catalogs = what_msx_catalogs()
    
    #testing msx_in_box
    #table = msx_in_box()
    
    #testing scattering
    scattering(table = table)
    