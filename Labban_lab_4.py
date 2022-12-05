#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import numpy.ma as ma
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.enums import Resampling
from rasterio.plot import show
from rasterio import Affine as A
from scipy.spatial import cKDTree
import random
import glob
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from scipy.spatial import ckdtree, kdtree


# In[2]:


shape = np.ones((11,9))
srcRst_PA = rasterio.open('./lab_4/data/protected_areas.tif')
srcRst_S = rasterio.open('./lab_4/data/slope.tif')
srcRst_UA = rasterio.open('./lab_4/data/urban_areas.tif')
srcRst_WB = rasterio.open('./lab_4/data/water_bodies.tif')
srcRst_80 = rasterio.open('./lab_4/data/ws80m.tif')


# In[3]:


files = glob.glob('./lab_4/data/*.tif')
files


# In[4]:


print("source raster crs: PA,S,UA,80")
print(srcRst_PA.crs, srcRst_S.crs, srcRst_UA.crs, srcRst_80.crs,"\n")
print("\rsource raster w/unkown crs: WB\n", srcRst_WB.crs)


# In[5]:


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

srcRst_PA = rasterio.open('./lab_4/data/protected_areas.tif')
print("source raster crs:")
print(srcRst_PA.crs)

dstCrs_PA = {'init': 'EPSG:4326'}
print("destination raster crs:")
print(dstCrs_PA)

transform, width, height = calculate_default_transform(
        srcRst_PA.crs, dstCrs_PA, srcRst_PA.width, srcRst_PA.height, *srcRst_PA.bounds)
print("transform array of source raster")
print(srcRst_PA.transform)

print("transform array of destination raster")
print(transform)


# In[6]:


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

srcRst_S = rasterio.open('./lab_4/data/slope.tif')
print("source raster crs:")
print(srcRst_S.crs)

dstCrs_S = {'init': 'EPSG:4326'}
print("destination raster crs:")
print(dstCrs_S)

transform, width, height = calculate_default_transform(
        srcRst_S.crs, dstCrs_S, srcRst_S.width, srcRst_S.height, *srcRst_S.bounds)
print("transform array of source raster")
print(srcRst_S.transform)

print("transform array of destination raster")
print(transform)


# In[7]:


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

srcRst_UA = rasterio.open('./lab_4/data/urban_areas.tif')
print("source raster crs:")
print(srcRst_UA.crs)

dstCrs_UA = {'init': 'EPSG:4326'}
print("destination raster crs:")
print(dstCrs_UA)

transform, width, height = calculate_default_transform(
        srcRst_UA.crs, dstCrs_UA, srcRst_UA.width, srcRst_UA.height, *srcRst_UA.bounds)
print("transform array of source raster")
print(srcRst_UA.transform)

print("transform array of destination raster")
print(transform)


# In[8]:


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

srcRst_80 = rasterio.open('./lab_4/data/water_bodies.tif')
print("source raster crs:")
print(srcRst_80.crs)

dstCrs_80 = {'init': 'EPSG:4326'}
print("destination raster crs:")
print(dstCrs_80)

transform, width, height = calculate_default_transform(
        srcRst_80.crs, dstCrs_80, srcRst_80.width, srcRst_80.height, *srcRst_80.bounds)
print("transform array of source raster")
print(srcRst_80.transform)

print("transform array of destination raster")
print(transform)


# In[9]:


kwargs = srcRst_PA.meta.copy()
kwargs.update({
        'crs': dstCrs_PA,
        'transform': transform,
        'width': width,
        'height': height
    })


# In[10]:


kwargs = srcRst_S.meta.copy()
kwargs.update({
        'crs': dstCrs_S,
        'transform': transform,
        'width': width,
        'height': height
    })


# In[11]:


kwargs = srcRst_UA.meta.copy()
kwargs.update({
        'crs': dstCrs_UA,
        'transform': transform,
        'width': width,
        'height': height
    })


# In[12]:


kwargs = srcRst_80.meta.copy()
kwargs.update({
        'crs': dstCrs_80,
        'transform': transform,
        'width': width,
        'height': height
    })


# In[13]:


dstRst_PA4326 = rasterio.open('./lab_4/data/data4326/protected_areas4326.tif', 'w', **kwargs)
dstRst_S4326 = rasterio.open('./lab_4/data/data4326/slope4326.tif', 'w', **kwargs)
dstRst_UA4326 = rasterio.open('./lab_4/data/data4326/urban_areas4326.tif', 'w', **kwargs)
drcRst_WB4326 = rasterio.open('./lab_4/data/data4326/water_bodies4326.tif', 'w', **kwargs)
dstRst_80_4326 = rasterio.open('./lab_4/data/data4326/ws80m4326.tif', 'w', **kwargs)


# In[14]:


print("source raster crs: dstRst,PA,S,UA,80")
print(dstRst_PA4326.crs, dstRst_S4326.crs, dstRst_UA4326.crs, drcRst_WB4326.crs, dstRst_80_4326.crs,"\n")
print("\rsource raster w/unkown crs: WB\n", srcRst_WB.crs)


# In[15]:


for i in range(1, srcRst_PA.count + 1):
    reproject(
        source=rasterio.band(srcRst_PA, i),
        destination=rasterio.band(dstRst_PA4326, i),
        src_crs_PA=srcRst_PA.crs,
        dst_crs_PA=dstCrs_PA,
        resampling=Resampling.nearest)

dstRst_PA4326.close()


# In[16]:


for i in range(1, srcRst_S.count + 1):
    reproject(
        source=rasterio.band(srcRst_S, i),
        destination=rasterio.band(dstRst_S4326, i),
        src_crs_S=srcRst_S.crs,
        dst_crs_S=dstCrs_S,
        resampling=Resampling.nearest)

dstRst_S4326.close()


# In[17]:


for i in range(1, srcRst_UA.count + 1):
    reproject(
        source=rasterio.band(srcRst_UA, i),
        destination=rasterio.band(dstRst_UA4326, i),
        src_crs_UA=srcRst_UA.crs,
        dst_crs_UA=dstCrs_UA,
        resampling=Resampling.nearest)
    
dstRst_UA4326.close()


# In[18]:


for i in range(1, srcRst_80.count + 1):
    reproject(
        source=rasterio.band(srcRst_80, i),
        destination=rasterio.band(dstRst_80_4326, i),
        src_crs_80=srcRst_80.crs,
        dst_crs_80=dstCrs_80,
        resampling=Resampling.nearest)

dstRst_80_4326.close()


# In[19]:


srcRst_PA = rasterio.open('./lab_4/data/protected_areas.tif')

arrayPA_PA = srcRst_PA.read(1)
print("old shape:",arrayPA_PA.shape)

dstRst_PA4326 = rasterio.open('./lab_4/data/data4326/protected_areas4326.tif')
arrayD_PA = dstRst_PA4326.read(1)

print("new shape:", arrayD_PA.shape,"current target:1825, 1116>1104")


# In[20]:


srcRst_S = rasterio.open('./lab_4/data/slope.tif')

arrayS_S = srcRst_S.read(1)
print("old shape:",arrayS_S.shape)

dstRst_S4326 = rasterio.open('./lab_4/data/data4326/slope4326.tif')
arrayD_S = dstRst_S4326.read(1)

print("new shape:", arrayD_S.shape,"current target:1825, 1116>1104")


# In[21]:


srcRst_UA = rasterio.open('./lab_4/data/urban_areas.tif')

arrayUA_UA = srcRst_UA.read(1)
print("old shape:",arrayUA_UA.shape)

dstRst_UA4326 = rasterio.open('./lab_4/data/data4326/urban_areas4326.tif')
arrayD_UA = dstRst_UA4326.read(1)

print("new shape:", arrayD_UA.shape,"current target:1825, 1116>1104")


# In[22]:


srcRst_80 = rasterio.open('./lab_4/data/ws80m.tif')

array80_80 = srcRst_80.read(1)
print("old shape:",array80_80.shape)

dstRst_80_4326 = rasterio.open('./lab_4/data/data4326/ws80m4326.tif')
arrayD_80 = dstRst_80_4326.read(1)

print("new shape:", arrayD_80.shape,"current target:1825, 1116>1104")


# In[36]:


def mean_filter(ma, mask):
    pct_array = np.zeros(ma.shape)
    win_area = float(mask.sum())
    row_dim = mask.shape[0]//2
    col_dim = mask.shape[1]//2
    for row in range(row_dim,ma.shape[0]-row_dim):
        for col in range(col_dim,ma.shape[1]-col_dim):
            win = ma[row-row_dim:row+row_dim+1,col-col_dim:col+col_dim+1]
            pct_array[row,col] = win.sum()
    return pct_array/win_area


# In[ ]:


## I was unable to complete the assignment due to the challanges I faced with it, this was quite a confusing lab to say the least. 
## I hope that I still have an oppertunity to get an 80% in the course so that I can get my GIS certificate. 
## Please let me know if there is anything I can do to raise my score on this lab, thank you.

