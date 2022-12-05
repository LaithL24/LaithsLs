#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
print(sys.prefix)


# In[2]:


pwd


# In[3]:


import glob
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.plot import show
from scipy import ndimage
from matplotlib import pyplot
from math import pi


# In[4]:


#Slope and Aspect Function
def slopeAspect(dem, cs):
    """Calculates slope and aspect using the 3rd-order finite difference method
    Parameters
    ----------
    dem : numpy array
        A numpy array of a DEM
    cs : float
        The cell size of the original DEM
    Returns
    -------
    numpy arrays
        Slope and Aspect arrays
    """
    #cs = Elk_dem.transform[0]
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    dzdx = ndimage.convolve(dem, kernel, mode='mirror') / (8 * cs)
    dzdy = ndimage.convolve(dem, kernel.T, mode='mirror') / (8 * cs)
    slp = np.arctan((dzdx ** 2 + dzdy ** 2) ** 0.5) * 180 / pi
    ang = np.arctan2(-dzdy, dzdx) * 180 / pi
    aspect = np.where(ang > 90, 450 - ang, 90 - ang)
    return slp, aspect


# In[5]:


#Reclassify Aspect
def reclassAspect(npArray):
    """Reclassify aspect array to 8 cardinal directions (N,NE,E,SE,S,SW,W,NW),
    encoded 1 to 8, respectively (same as ArcGIS aspect classes).
    Parameters
    ----------
    npArray : numpy array
        numpy array with aspect values 0 to 360
    Returns
    -------
    numpy array
        numpy array with cardinal directions
    """
    return np.where((npArray > 22.5) & (npArray <= 67.5), 2,
    np.where((npArray > 67.5) & (npArray <= 112.5), 3,
    np.where((npArray > 112.5) & (npArray <= 157.5), 4,
    np.where((npArray > 157.5) & (npArray <= 202.5), 5,
    np.where((npArray > 202.5) & (npArray <= 247.5), 6,
    np.where((npArray > 247.5) & (npArray <= 292.5), 7,
    np.where((npArray > 292.5) & (npArray <= 337.5), 8, 1)))))))


# In[6]:


#Reclass array function
def reclassByHisto(npArray, bins):
    """Reclassify np array based on a histogram approach using a specified
    number of bins. Returns the reclassified numpy array and the classes from
    the histogram.
    Parameters
    ----------
    npArray : numpy array
        Array to be reclassified
    bins : int
        Number of bins
    Returns
    -------
    numpy array
        umpy array with reclassified values
    """
    histo = np.histogram(npArray, bins)[1]
    rClss = np.zeros_like(npArray)
    for i in range(bins):
        rClss = np.where((npArray >= histo[i]) & (npArray <= histo[i + 1]),
                         i + 1, rClss)
    return rClss


# In[7]:


#Opens rasters, defines variables
Elk_dem = rasterio.open('./lab_5/data/bigElk_dem.tif')
fire_perimeter = rasterio.open('./lab_5/data/fire_perimeter.tif')
glob.glob('./lab_5/data/L5_big_elk/*tif')


# In[8]:


#Creates arrays
Elk_array = Elk_dem.read(1)
fire_array = fire_perimeter.read(1)


# In[9]:


#Applies the given functions
aspect, slope = slopeAspect(Elk_array, Elk_dem.transform[0])
aspect_reclass = reclassAspect(aspect)
slope_reclass = reclassByHisto(slope, 10)


# In[10]:


#Defines red and infrared bands
red = glob.glob('./lab_5/data/L5_big_elk/*B3.tif')
ifr = glob.glob('./lab_5/data/L5_big_elk/*B4.tif')
Nburned = np.where(fire_array == 2)
burned = np.where(fire_array ==1)


# In[11]:


#Creates empty lists 
#Recovery Ratio = RRatio = (NDVIij)/(mean(NDVI of healthy forest))
meanlist = []
RRlist = []
years = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11']


# In[12]:


#Part 1
for x,y in zip(red, ifr):
    red = rasterio.open(x,'r').read(1)
    ifr = rasterio.open(y,'r').read(1)
    ndvi = ((ifr-red)/(ifr+red))
    ndvi_mean = ndvi[Nburned].mean()
    RRatio = ndvi/ndvi_mean
    burn_mean = RRatio[burned].mean()
    meanlist.append(burn_mean)
    ravRRatio = RRatio.ravel()
    RRlist.append(ravRRatio)
RRliststack = np.vstack(RRlist)
line = np.polyfit(range(10), RRliststack, 1)[0]
#np.shape(red)(or ifr) (280, 459)
line_reshape = line.reshape(280, 459)
FCoefficient = np.where(fire_array==1, line_reshape, np.nan)
print('Coefficient of recovery ratio for 02-11 is', np.nanmean(FCoefficient))
for w,z in zip(years, meanlist):
    print('Recovery ratio for', w, 'is', round(np.nanmean(z),5))


# In[13]:


#Part 2
#Zonal stats function 
#slope and aspect csv files
MC = np.nanmean(FCoefficient)
def ZStatsTable(ZRaster, VRaster, output):
    means = []
    sd = []
    mins = []
    maxs = []
    counts = []
    for x in np.unique(ZRaster):
        zonal = np.where(ZRaster == x, x, np.nan)
        means.append(np.nanmean(zonal * VRaster))
        sd.append(np.nanstd(zonal * VRaster))
        mins.append(np.nanmin(zonal * VRaster))
        maxs.append(np.nanmax(zonal * VRaster))
        counts.append(np.where(ZRaster == x, 1, 0 ).sum())
    ZStats = {'means': means, 'standard deviation': sd, 'mins': mins, 'maxs': maxs, 'counts': counts}
    #print(type(ZStats)) = 'dict'
    ZSdf=pd.DataFrame(ZStats)
    ZSdf.to_csv(output)
    return ZSdf
ZStatsTable(slope_reclass, MC, 'slope.csv')
ZStatsTable(aspect_reclass, MC, 'aspect.csv')


# In[23]:


#Export new tif representing the new data!
with rasterio.open('./lab_5/data/bigElk_dem.tif') as data:
    with rasterio.open('FCoefficient.tif', 'w', driver='GTiff',
                          height=FCoefficient.shape[0],
                          width=FCoefficient.shape[1],
                          count=1,
                          dtype=np.float64,
                          crs=data.crs,
                       transform=data.transform,
                        nodata=data.nodata) as Ndata:
        Ndata.write(FCoefficient,1)


# In[15]:


with rasterio.open('./FCoefficient.tif') as Fdata:
    FINAL = Fdata.read(1)
show(FINAL)


# In[30]:


print('Based on the analysis of the aspect, southern and southeastern had a stronger recovery. \n', 
      'Additionally, the areas with lower slopes had the better overall recovery.')

